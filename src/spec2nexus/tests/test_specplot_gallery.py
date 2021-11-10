"""Tests for the specplot_gallery module."""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

import json
from lxml import etree
import os
import pytest
import shutil
import sys
import time

from . import _core
from ._core import tempdir
from .. import specplot_gallery


ARGV0 = sys.argv[0]
SHORT_DELAY = 0.1  # allo time for OS to update mtime


def abs_data_fname(fname):
    return os.path.join(_core.EXAMPLES_DIR, fname)


def test_command_line_NeXus_writer_1_3(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-d", tempdir, abs_data_fname("writer_1_3.h5")]

    specplot_gallery.main()

    # this is HDF5 file, not SPEC, so no content
    children = os.listdir(tempdir)
    assert len(children) == 0


def test_command_line_spec_data_file_33bm_spec(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-d", tempdir, abs_data_fname("33bm_spec.dat")]

    specplot_gallery.main()

    assert os.path.exists(os.path.join(tempdir, specplot_gallery.MTIME_CACHE_FILE))
    # TODO: test contents of mtime_cache.txt?

    plot_path = os.path.join(tempdir, "2010", "06", "33bm_spec")
    assert os.path.exists(plot_path)
    assert os.path.exists(os.path.join(plot_path, "33bm_spec.dat"))

    web_page = os.path.join(plot_path, "index.html")
    assert os.path.exists(web_page)
    # TODO: #69: look for handling of scan 15


def test_command_line_spec_data_file_user6idd(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-d", tempdir, abs_data_fname("user6idd.dat")]

    specplot_gallery.main()

    assert os.path.exists(os.path.join(tempdir, specplot_gallery.MTIME_CACHE_FILE))

    # S1 aborted, S2 all X,Y are 0,0
    plot_path = os.path.join(tempdir, "2013", "10", "user6idd")
    assert os.path.exists(plot_path)
    assert os.path.exists(os.path.join(plot_path, "user6idd.dat"))
    assert os.path.exists(os.path.join(plot_path, "index.html"))
    # TODO: #69: look for handling of scan 1


def test_command_line_spec_data_file_03_06_JanTest(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-d", tempdir, abs_data_fname("03_06_JanTest.dat")]

    specplot_gallery.main()

    assert os.path.exists(os.path.join(tempdir, specplot_gallery.MTIME_CACHE_FILE))

    # S1 aborted, S2 all X,Y are 0,0
    plot_path = os.path.join(tempdir, "2014", "03", "03_06_JanTest")
    assert os.path.exists(plot_path)
    assert os.path.exists(os.path.join(plot_path, "03_06_JanTest.dat"))
    assert os.path.exists(os.path.join(plot_path, "index.html"))
    assert os.path.exists(os.path.join(plot_path, "s00001" + specplot_gallery.PLOT_TYPE))
    # TODO: #69: look for handling of scan 1
    assert not os.path.exists(os.path.join(plot_path, "s1" + specplot_gallery.PLOT_TYPE))
    # TODO: look for that scan in index.html?


def test_command_line_spec_data_file_02_03_setup(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-d", tempdir, abs_data_fname("02_03_setup.dat")]

    specplot_gallery.main()

    assert os.path.exists(os.path.join(tempdir, specplot_gallery.MTIME_CACHE_FILE))

    plot_path = os.path.join(tempdir, "2016", "02", "02_03_setup")
    assert os.path.exists(plot_path)
    assert os.path.exists(os.path.join(plot_path, "02_03_setup.dat"))
    web_page = os.path.join(plot_path, "index.html")
    assert os.path.exists(web_page)
    # TODO: #69: look for handling of scan 5

    # look for diagnostics in first web page comment element
    doc = etree.parse(web_page)
    for element in doc.iter():
        if element.__class__.__name__ == "_Comment":
            comments = element.text.splitlines()
            assert len(comments) >= 3
            catalog = {
                line.strip().split()[0].strip(":"): line.strip()
                for line in comments
                if len(line.strip()) > 0
            }
            expected = "written date workstation username version pid"
            for k in expected.split():
                assert k in catalog, k

            break


def test_command_line_spec_data_file_list(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-d", tempdir]

    for item in "user6idd.dat APS_spec_data.dat 02_03_setup.dat".split():
        sys.argv.append(abs_data_fname(item))

    specplot_gallery.main()

    assert os.path.exists(os.path.join(tempdir, specplot_gallery.MTIME_CACHE_FILE))

    plot_path = os.path.join(tempdir, "2010", "11", "APS_spec_data")
    assert os.path.exists(plot_path)
    for item in "APS_spec_data.dat   index.html".split():
        assert os.path.exists(os.path.join(plot_path, item))

    plot_path = os.path.join(tempdir, "2013", "10", "user6idd")
    assert os.path.exists(plot_path)
    for item in "user6idd.dat   index.html".split():
        assert os.path.exists(os.path.join(plot_path, item))

    plot_path = os.path.join(tempdir, "2016", "02", "02_03_setup")
    assert os.path.exists(plot_path)
    for item in "02_03_setup.dat   index.html".split():
        assert os.path.exists(os.path.join(plot_path, item))


def test_command_line_spec_data_file_list_reversed_chronological_issue_79(tempdir):
    assert os.path.exists(tempdir)
    sys.argv = [ARGV0, "-r", "-d", tempdir, abs_data_fname("APS_spec_data.dat")]

    specplot_gallery.main()

    plot_path = os.path.join(tempdir, "2010", "11", "APS_spec_data")
    assert os.path.exists(plot_path)
    for item in "APS_spec_data.dat   index.html".split():
        assert os.path.exists(os.path.join(plot_path, item))


def test_command_line_specified_directory_not_found_issue_98():
    sys.argv = [ARGV0, "-d", "Goofball-directory_does_not_exist", abs_data_fname("APS_spec_data.dat")]

    with pytest.raises(specplot_gallery.DirectoryNotFoundError):
        specplot_gallery.main()


def test_command_line_specified_directory_fails_isdir_issue_98(tempdir):
    text_file_name = os.path.join(tempdir, "goofball.txt")
    with open(text_file_name, "w") as outp:
        outp.write("goofball text is not a directory")

    sys.argv = [ARGV0, "-d", text_file_name, abs_data_fname("APS_spec_data.dat")]

    with pytest.raises(specplot_gallery.PathIsNotDirectoryError):
        specplot_gallery.main()


def test_refresh(tempdir):
    spec_file = _core.getActiveSpecDataFile(tempdir)
    assert os.path.exists(spec_file)

    gallery = os.path.join(tempdir, "gallery")
    assert not os.path.exists(gallery)

    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    assert os.path.exists(gallery)
    assert os.path.exists(
        os.path.join(gallery, specplot_gallery.MTIME_CACHE_FILE)
    )

    def children_mtimes(plotdir, children):
        return {
            k: os.path.getmtime(os.path.join(plotdir, k))
            for k in children
        }

    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    plotdir = os.path.join(gallery, "2010", "11", "specdata")
    assert os.path.exists(gallery)
    assert os.path.exists(os.path.join(gallery, "2010"))
    assert os.path.exists(os.path.join(gallery, "2010", "11"))
    # assert os.listdir(os.path.join(gallery, "2010", "11")) == []
    assert os.path.exists(os.path.join(gallery, "2010", "11", "specdata"))
    assert os.path.exists(plotdir)
    children = [
        k
        for k in sorted(os.listdir(plotdir))
        if k.endswith(specplot_gallery.PLOT_TYPE)
    ]
    assert len(children) == 3
    mtimes = children_mtimes(plotdir, children)
    assert len(mtimes) == 3

    # update the file with more data
    _core.addMoreScans(spec_file)
    time.sleep(SHORT_DELAY)

    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    k = children[-1]
    assert os.path.getmtime(os.path.join(plotdir, k)) != mtimes[k], k
    for k in children[:-1]:
        # should pass all but the latest (#S 3)
        assert os.path.getmtime(os.path.join(plotdir, k)) == mtimes[k], k
    children = [
        k
        for k in sorted(os.listdir(plotdir))
        if k.endswith(specplot_gallery.PLOT_TYPE)
    ]
    mtimes = children_mtimes(plotdir, children)
    assert len(children) == 5

    # update the file with another scan
    _core.addMoreScans(spec_file, "refresh3.txt")
    time.sleep(SHORT_DELAY)

    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    children = [
        k
        for k in sorted(os.listdir(plotdir))
        if k.endswith(specplot_gallery.PLOT_TYPE)
    ]
    assert len(children) == 6
    for k in children[:-2]:
        # should pass all but last 2 scans (refresh last existing plus one new)
        assert os.path.getmtime(os.path.join(plotdir, k)) == mtimes[k], k

    # restart file with first set of scans, should trigger replot all
    t0 = time.time()
    time.sleep(SHORT_DELAY)
    src = os.path.join(_core.TEST_DATA_DIR, "refresh1.txt")
    shutil.copy(src, spec_file)

    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    children = [
        k
        for k in sorted(os.listdir(plotdir))
        if k.endswith(specplot_gallery.PLOT_TYPE)
    ]
    assert len(children) == 3
    for k in children:
        # should pass all
        assert os.path.getmtime(os.path.join(plotdir, k)) > t0, k

    _core.addMoreScans(spec_file)
    time.sleep(SHORT_DELAY)
    specplot_gallery.PlotSpecFileScans([spec_file], gallery)

    # restart file again, use reversed chronological order
    t0 = time.time()
    time.sleep(SHORT_DELAY)
    src = os.path.join(_core.TEST_DATA_DIR, "refresh1.txt")
    shutil.copy(src, spec_file)

    specplot_gallery.PlotSpecFileScans(
        [spec_file], gallery, reverse_chronological=True
    )
    assert len(children) == 3
    _core.addMoreScans(spec_file)
    time.sleep(SHORT_DELAY)
    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    children = [
        k
        for k in sorted(os.listdir(plotdir))
        if k.endswith(specplot_gallery.PLOT_TYPE)
    ]

    # issue #206 here
    # edit mtime_cache.json
    mtime_file = os.path.join(
        gallery, specplot_gallery.MTIME_CACHE_FILE
    )
    assert os.path.exists(mtime_file)
    with open(mtime_file, "r") as fp:
        mtimes = json.loads(fp.read())
    # edit mtimes
    mtimes[spec_file]["mtime"] = 1
    mtimes[spec_file]["size"] = 1
    with open(mtime_file, "w") as fp:
        fp.write(json.dumps(mtimes, indent=4))
    # reprocess
    specplot_gallery.PlotSpecFileScans([spec_file], gallery)
    # list of all available plot images
    plots = [
        f
        for f in sorted(os.listdir(plotdir))
        if f.endswith(specplot_gallery.PLOT_TYPE)
    ]
    # look at the index.html file
    index_file = os.path.join(
        plotdir, specplot_gallery.HTML_INDEX_FILE
    )
    with open(index_file, "r") as fp:
        html = fp.read()
    for line in html.splitlines():
        if line.endswith(" plotted scan(s)</h2>"):
            n = int(line.strip()[4:].split()[0])
            assert n >= 0
            assert n == len(plots)
        elif line.find(specplot_gallery.PLOT_TYPE) > 0:
            for plot in plots:
                if line.find(plot) < 0:
                    continue
                msg = "plot %s is not linked" % str(plot)
                msg += " in `%s`" % specplot_gallery.HTML_INDEX_FILE
                assert line.startswith("<a href="), msg
