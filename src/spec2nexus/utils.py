# -*- coding: utf-8 -*-

"""
(internal library) common methods used in **spec2nexus** modules

.. autosummary::

    ~clean_name
    ~iso8601
    ~reshape_data
    ~sanitize_name
    ~split_column_labels
    ~split_scan_number_string
    ~strip_first_word

"""

import logging
import numpy
import re
import time


logger = logging.getLogger(__name__)


def clean_name(key):
    """
    create a name that is allowed by both HDF5 and NeXus rules

    :param str key: identifying string from SPEC data file

    :see: https://download.nexusformat.org/doc/html/datarules.html

    The "sanitized" name fits this regexp::

        [A-Za-z_][\w_]*

    An easier expression might be:  ``[\w_]*`` but this will not pass
    the rule that valid NeXus group or field names cannot start with a digit.
    """
    replacement = "_"
    noncompliance = r"[^\w_]"
    txt = replacement.join(
        re.split(noncompliance, key)
    )  # replace ALL non-compliances with '_'
    if txt[0].isdigit():
        txt = replacement + txt  # can't start with a digit
    return txt


def iso8601(date):
    """
    convert SPEC time (example: Wed Nov 03 13:39:34 2010) into ISO8601 string

    :param str date: time string from SPEC data file

    **Example**

    :SPEC:    Wed Nov 03 13:39:34 2010
    :ISO8601: 2010-11-03T13:39:34
    :SPOCK:   09/15/17 04:39:10
    :ISO8601: 2017-09-15T04:39:10
    """
    spec_fmt = "%a %b %d %H:%M:%S %Y"
    try:
        t_obj = time.strptime(date, spec_fmt)
    except ValueError:
        spock_fmt = "%m/%d/%y %H:%M:%S"
        try:
            t_obj = time.strptime(date, spock_fmt)
        except ValueError as ex:
            raise ex
    iso_fmt = "%Y-%m-%dT%H:%M:%S"
    iso = time.strftime(iso_fmt, t_obj)
    return iso


def strip_first_word(line):
    """return everything after the first space on the line from the spec data file"""
    pos = line.find(" ")
    val = line[pos:]
    return val.strip()


def split_column_labels(text):
    """SPEC labels may contain one space"""
    return re.split("  +", text.replace("\t", "  "))


def split_scan_number_string(key):
    """
    Split a string scan number into its parts.

    key str:
        A value from the list returned by :meth:`~spec2nexus.spec.SpecDataFile.getScanNumbers()`.
    returns:
        tuple of (`#S` number, repeat occurrence number)

    EXAMPLES::

        >>> split_scan_number_string("0")
        (0, 0)
        >>> split_scan_number_string("0.5")
        (0, 5)
    """
    # rstrip(".") is for pathological key="0."
    parts = list(map(int, str(key).rstrip(".").split(".")))
    if len(parts) == 0:
        parts = [0]
    if len(parts) == 1:
        parts.append(0)
    return tuple(parts)


def sanitize_name(group, key):  # for legacy support only
    """make name that is allowed by HDF5 and NeXus rules

    :note: **deprecated**  use :func:`clean_name` instead (``group`` is never used)
    :param str group: unused
    :param str key: identifying string from SPEC data file

    :see: https://download.nexusformat.org/doc/html/datarules.html

    sanitized name fits this regexp::

        [A-Za-z_][\w_]*

    An easier expression might be:  ``[\w_]*`` but this will not pass
    the rule that valid names cannot start with a digit.
    """
    return clean_name(key)


def reshape_data(scan_data, scan_shape):
    """
    Shape scan data from raw to different dimensionality

    Some SPEC macros collect data in a mesh or grid yet
    report the data as a 1-D sequence of observations.
    For further processing (such as plotting), the scan data
    needs to be reshaped according to its intended dimensionality.

    modified from nexpy.readers.readspec.reshape_data
    """
    scan_size = numpy.prod(scan_shape)
    if scan_data.size == scan_size:
        data = scan_data
    elif scan_data.size < scan_size:
        data = numpy.empty(scan_size)
        data.fill(numpy.NaN)  # pad data with NaN
        data[0: scan_data.size] = scan_data.ravel()  # flatten & insert
    else:
        data = scan_data.ravel()  # flatten
        data = data[0:scan_size]  # truncate extra data
    return data.reshape(scan_shape)

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
