"""
Describe SPEC diffractometer geometry #G control lines.

  #G0 ...       G[] array (geo mode, sector, etc)
  #G1 ...       U[] array (lattice constants, orientation reflections)
  #G2 is unused
  #G3 ...       UB[] array (orientation matrix)
  #G4 ...       Q[] array (lambda, frozen angles, cut points, etc)

API

.. autosummary::

    ~Diffractometer
    ~DiffractometerGeometryCatalog
    ~split_name_variation
    ~get_geometry_catalog
    ~reset_geometry_catalog

"""

from collections import namedtuple, OrderedDict
import datetime
import logging
import numpy
import pathlib


logger = logging.getLogger(__name__)
_path = pathlib.Path(__file__).parent
DICT_FILE = _path / "diffractometer-geometries.dict"


KeyDescriptionValue = namedtuple(
    "KeyDescriptionValue", "key description value"
)

LatticeParameters2D = namedtuple(
    "LatticeParameters2D", "a b gamma"
)

LatticeParameters3D = namedtuple(
    "LatticeParameters3D", "a b c alpha beta gamma"
)

Reflections2D = namedtuple("Reflections2D", "h k wavelength angles")

Reflections3D = namedtuple("Reflections3D", "h k l wavelength angles")


# lattice constants, orientation reflections
# most geometries use this default schema
# at least one geometry (twoc) has overrides
DEFAULT_U = [
    ("g_aa", "a lattice constant (real space)"),
    ("g_bb", "b lattice constant (real space)"),
    ("g_cc", "c lattice constant (real space)"),
    ("g_al", "alpha lattice angle (real space)"),
    ("g_be", "beta  lattice angle (real space)"),
    ("g_ga", "gamma lattice angle (real space)"),
    ("g_aa_s", "a lattice constant (reciprocal space)"),
    ("g_bb_s", "b lattice constant (reciprocal space)"),
    ("g_cc_s", "c lattice constant (reciprocal space)"),
    ("g_al_s", "alpha lattice angle (reciprocal space)"),
    ("g_be_s", "beta  lattice angle (reciprocal space)"),
    ("g_ga_s", "gamma lattice angle (reciprocal space)"),
    ("g_h0", "H of primary reflection"),
    ("g_k0", "K of primary reflection"),
    ("g_l0", "L of primary reflection"),
    ("g_h1", "H of secondary reflection"),
    ("g_k1", "K of secondary reflection"),
    ("g_l1", "L of secondary reflection"),
    ("g_u00", "angle 0 of primary reflection"),
    ("g_u01", "angle 1 of primary reflection"),
    ("g_u02", "angle 2 of primary reflection"),
    ("g_u03", "angle 3 of primary reflection"),
    ("g_u04", "angle 4 of primary reflection"),
    ("g_u05", "angle 5 of primary reflection"),
    ("g_u10", "angle 0 of secondary reflection"),
    ("g_u11", "angle 1 of secondary reflection"),
    ("g_u12", "angle 2 of secondary reflection"),
    ("g_u13", "angle 3 of secondary reflection"),
    ("g_u14", "angle 4 of secondary reflection"),
    ("g_u15", "angle 5 of secondary reflection"),
    ("g_lambda0", "lambda when or0 was set"),
    ("g_lambda1", "lambda when or1 was set"),
    # For backward compatibility, additional angles added at end of array
    ("g_u06", "optional, angle 6 of primary reflection"),
    ("g_u16", "optional, angle 6 of secondary reflection"),
]


def split_name_variation(geo_name):
    """
    split geo_name into geometry name and variation
    """
    nm = geo_name
    try:
        nm, variant = geo_name.split(".")
    except ValueError:
        variant = None
    return nm, variant


class Diffractometer:
    """
    describe the diffractometer for the scan

    .. autosummary::

        ~parse
        ~print_all
        ~print_brief
    """

    def __init__(self, geo_name):
        self.geometry_name_full = geo_name
        self.geometry_name, self.variant = split_name_variation(geo_name)
        self.geometry_parameters = {}  # combined #G terms
        self.lattice = None
        self.mode = None
        self.reflections = []
        self.sector = None
        self.wavelength = None

        gpar = self.geometry_parameters
        gpar["diffractometer_full"] = KeyDescriptionValue(
            "diffractometer_full",
            "name of diffractometer (and variant), deduced from scan information",
            self.geometry_name_full,
        )
        gpar["diffractometer_simple"] = KeyDescriptionValue(
            "diffractometer_simple",
            "name of diffractometer, deduced from scan information",
            self.geometry_name,
        )
        gpar["diffractometer_variant"] = KeyDescriptionValue(
            "diffractometer_variant",
            "name of diffractometer variant, deduced from scan information",
            self.variant or "",
        )

    def _get_info_dict(self, level="str"):
        """
        Return dictionary for use in various reports.

        PARAMETER

        level str :
            Level of detail for desired report.
            One of these values: ``pa``, ``str``, ``wh``.
            Default: ``str``
        """
        info = {}
        gpars = self.geometry_parameters

        info["geometry"] = f"'{self.geometry_name}'"
        info["wavelength"] = f"{self.wavelength}"
        info["mode"] = f"'{self.mode}'"
        info["sector"] = f"{self.sector}"
        for key in self._Q_names:
            info[key] = f"{gpars[key.upper()].value}"

        if level in ("pa", "wh"):
            info["lattice"] = f"{self.lattice}"
            for key in "alpha beta azimuth omega".split():  # TODO: generalize per issue #274
                if key.upper() in gpars:
                    info[key.lower()] = f"{gpars[key.upper()].value}"

        if level in ("pa", ):
            full_name = self.geometry_name_full
            info["full_geometry_name"] = f"'{full_name}'"
            if hasattr(self, "lattice") and self.lattice is not None:
                info["lattice"] = f"{self.lattice}"
            if hasattr(self, "UB"):
                info["UB"] = self.UB
            if hasattr(self, "reflections"):
                for i, refl in enumerate(self.reflections, start=1):
                    info[f"reflection {i}"] = f"{refl}"
                info["UB"] = self.UB

        return info

    def __str__(self):
        """
        Brief representation of this diffractometer.
        """
        s = [f"{k}={v}" for k, v in self._get_info_dict().items()]
        return f"Diffractometer({', '.join(s)})"

    @property
    def _Q_names(self):
        """
        List of names used to define Q (typically: h k l).  All lower case.
        """
        geometry = get_geometry_catalog().get(self.geometry_name_full)
        return [
            q_term[0].lower()
            for q_term in geometry["Q"]
            if "Miller index" in q_term[1]
        ]

    def _positioners_dict(self, scan):
        """
        Dictionary with positioners (keys) and positions (values) in this scan.

        PARAMETERS

        scan obj :
            SPEC data file scan (a ``spec2nexus.spec.SpecDataFileScan`` object).
        """
        geometry = get_geometry_catalog().get(self.geometry_name_full)
        number_motors_in_geometry = geometry["numgeo"]
        return {
            k: scan.positioner[k]
            for k in list(scan.positioner.keys())[:number_motors_in_geometry]
        }

    def _get_Q_dict(self, info):
        """
        Dictionary with all the Q-related terms & values (hkl, for example).

        PARAMETERS

        info dict :
            from `_get_info_dict()`
        """
        return {key: info[key] for key in self._Q_names}

    def parse(self, scan):
        dgc = DiffractometerGeometryCatalog()
        gonio = dgc.get(self.geometry_name_full)

        G = OrderedDict()
        if "G0" in scan.G:
            g0 = list(map(float, scan.G["G0"].split()))
            if len(g0) == len(gonio["G"]):
                G = OrderedDict(
                    {
                        kd[0]: KeyDescriptionValue(kd[0], kd[1], v)
                        for v, kd in zip(g0, gonio["G"])
                    }
                )
                additions = []
                for k, kdv in G.items():
                    if k.startswith("g_sect"):
                        self.sector = int(kdv.value)
                        continue
                    if not k.startswith("g_mode"):
                        continue
                    modes = gonio["modes"]
                    if not (0 <= int(kdv.value) < len(modes)):
                        continue
                    entry = KeyDescriptionValue(
                        k + "_name",
                        "name of " + kdv.description,
                        modes[int(kdv.value)],
                    )
                    additions.append(entry)
                # must update G{} in two steps
                for entry in additions:
                    G[entry.key] = entry
                    if entry.key == "g_mode_name":
                        self.mode = entry.value
        self.geometry_parameters.update(G)

        if "G1" in scan.G:
            g1 = list(map(float, scan.G["G1"].split()))
            if len(g1) > 1:
                # at least one geometry overrides the default U[] terms
                gonio_U = gonio.get("U", list(DEFAULT_U))
                U = OrderedDict(
                    {
                        kd[0]: KeyDescriptionValue(kd[0], kd[1], v)
                        for v, kd in zip(g1, gonio_U)
                    }
                )
                if ("g_cc" in U) and ("g_al" in U) and ("g_be" in U):
                    _parms = [U[f"g_{key}"].value for key in "aa bb cc al be ga".split()]
                    self.lattice = LatticeParameters3D(*_parms)
                else:  # twoc
                    _parms = [U[f"g_{key}"].value for key in "aa bb ga".split()]
                    self.lattice = LatticeParameters2D(*_parms)
                for ref_num in (0, 1):
                    template = "g_u%d%%d" % ref_num
                    variant = dgc.get_variant(gonio, self.variant)
                    angles = OrderedDict()
                    for i, mne in enumerate(variant["motors"]):
                        k = template % i
                        if k in U:
                            angles[mne] = U[k].value
                    if ("g_lambda" not in U):
                        _parms = [U[f"g_{k}{ref_num}"].value for k in "h k l lambda".split()]
                        _parms.append(angles)
                        ref = Reflections3D(*_parms)
                    else:  # twoc
                        if ref_num > 0:
                            break  # at most, 1 reflection is defined
                        _parms = [U[f"g_{k}{ref_num}"].value for k in "h k".split()]
                        _parms.append(U["g_lambda"].value)
                        _parms.append(angles)
                        ref = Reflections2D(*_parms)
                    self.reflections.append(ref)

                self.geometry_parameters.update(U)

        if "G3" in scan.G:
            g3 = list(map(float, scan.G["G3"].split()))
            if len(g3) == 9:
                UB = numpy.array(g3).reshape((3, 3))
                self.geometry_parameters[
                    "ub_matrix"
                ] = KeyDescriptionValue("ub_matrix", "UB[] matrix", UB)
                self.UB = UB

        Q = OrderedDict()
        if "G4" in scan.G:
            g4 = list(map(float, scan.G["G4"].split()))
            if len(g4) == len(gonio["Q"]):
                Q = OrderedDict(
                    {
                        kd[0]: KeyDescriptionValue(kd[0], kd[1], v)
                        for v, kd in zip(g4, gonio["Q"])
                    }
                )
                if "LAMBDA" in Q:
                    self.wavelength = Q["LAMBDA"].value
        self.geometry_parameters.update(Q)

    def print_all(self, scan):
        """
        Print All (pa) about this diffractometer scan.

        PARAMETERS

        scan obj :
            SPEC data file scan (a ``spec2nexus.spec.SpecDataFileScan`` object).
        """
        scan.interpret()
        s = {
            "SPEC file": scan.specFile,
            "scan #": scan.scanNum,
            "SPEC scanCmd": scan.scanCmd,
        }
        if hasattr(scan, "epoch"):
            s["date"] = datetime.datetime.fromtimestamp(scan.epoch)
        s.update(self._get_info_dict("pa"))
        s.update(self._positioners_dict(scan))

        width = max([len(k) for k in s.keys()])
        return '\n'.join([f"{k:^{width}} = {v}" for k, v in s.items()])

    def print_brief(self, scan):
        """
        Print brief information (wh: where) about this diffractometer scan.

        PARAMETERS

        scan obj :
            SPEC data file scan (a ``spec2nexus.spec.SpecDataFileScan`` object).
        """
        info = self._get_info_dict("wh")
        qdict = self._get_Q_dict(info)

        s = []

        s.append(info["geometry"].strip("'"))

        if len(qdict):
            label = f"{' '.join([k for k in qdict.keys()])}"
            r = f"{'  '.join(qdict.values())}"
            s.append(f"{label} = {r}")

        def _compose_row_(labels):
            return "  ".join(
                [
                    f"{k}={info[k]}"
                    for k in labels
                    if k in info
                ]
            )

        s.append(_compose_row_("alpha beta azimuth".split()))
        s.append(_compose_row_("omega wavelength".split()))

        for k, v in self._positioners_dict(scan).items():
            s.append(f"{k} = {v}")

        return '\n'.join(s)


# singleton reference to DiffractometerGeometryCatalog
_geometry_catalog = None


def get_geometry_catalog():
    global _geometry_catalog
    if _geometry_catalog is None:
        _geometry_catalog = 0
        _geometry_catalog = DiffractometerGeometryCatalog()
    return _geometry_catalog


def reset_geometry_catalog():
    global _geometry_catalog
    _geometry_catalog = None


class DiffractometerGeometryCatalog:
    """
    catalog of the diffractometer geometries known to SPEC

    .. autosummary::

        ~geometries
        ~get
        ~get_default_geometry
        ~has_geometry
        ~match
    """

    db = {}

    def __init__(self):
        if _geometry_catalog is None:
            raise RuntimeError(
                "Do not create DiffractometerGeometryCatalog()."
                "  Instead, call: get_geometry_catalog()"
                # don't call that here, _geometry_catalog is a singleton
            )

        with open(DICT_FILE, "r") as fp:
            self.db = eval(fp.read())

        self._default_geometry = self.db[0]
        self._geometries_simple = None
        self._geometries_full = None

    def __str__(self):
        v = "number=" + str(len(self.db))
        s = "DiffractometerGeometryCatalog(%s)" % v
        return s

    def geometries(self, variations=False):
        """
        list known geometries

        PARAMETERS

        variations : bool
            If True, also list known variations
        """
        if (
            self._geometries_simple is None
            and self._geometries_full is None
        ):
            # optimize with a cache, construct only once
            self._geometries_simple, self._geometries_full = [], []
            for geometry in self.db:
                nm = geometry["name"]
                self._geometries_full += [
                    "%s.%s" % (nm, v["name"])
                    for v in geometry["variations"]
                ]
                self._geometries_simple.append(nm)

        choices = {
            True: self._geometries_full,
            False: self._geometries_simple,
        }
        return choices[variations]

    def get(self, geo_name, default=None):
        """
        return dictionary for diffractometer geometry ``geo_name``
        """
        nm = split_name_variation(geo_name)[0]
        geometries = self.geometries()
        if nm in geometries:
            return self.db[geometries.index(nm)]
        return default

    def get_default_geometry(self):
        " "
        return self._default_geometry

    def get_variant(self, geometry, variant_name):
        " "
        for v in geometry["variations"]:
            if v["name"] == variant_name:
                return v
        return geometry["variations"][0]

    def has_geometry(self, geo_name):
        """
        Is the ``geo_name`` geometry defined?  True or False
        """
        nm, variant = split_name_variation(geo_name)
        if variant is None:
            return nm in self.geometries()
        else:
            return geo_name in self.geometries(True)

    def _get_scan_positioners_(self, scan):
        scan_positioners = []
        if hasattr(scan.header, "o"):  # prefer mnemonics
            for row in scan.header.o:
                scan_positioners += row
        elif hasattr(scan.header, "O"):
            for row in scan.header.O:
                scan_positioners += [k.lower() for k in row]
        else:
            scan_positioners = [k.lower() for k in scan.positioner.keys()]
        if len(scan_positioners) > 0:
            scan_positioners_new = []
            for k in scan_positioners:
                if k in ("2-theta", "two theta") or k.endswith("tth"):
                    k = "tth"
                elif k in ("theta",):
                    k = "th"
                elif k in ("delta",):
                    k = "del"
                elif k in ("gamma",):
                    k = "gam"
                scan_positioners_new.append(k)
            scan_positioners = scan_positioners_new

        return scan_positioners

    def match(self, scan):
        """
        find the ``geo_name`` geometry that matches the ``scan``

        If there is more than one matching geometry, pick the first one.
        """
        match = []

        scan_positioners = self._get_scan_positioners_(scan)

        if hasattr(scan, "G"):
            scan_G0 = scan.G.get("G0", "0").split()
            if scan_G0 == [
                "0",
            ]:
                scan_G0 = []

            if "G4" in scan.G:
                scan_G4 = scan.G["G4"].split()
                if scan_G4 == [
                    "0",
                ]:
                    scan_G4 = []
            else:
                scan_G4 = None

        else:
            scan_G0, scan_G4 = None, None

        for geometry in self.db:
            geo_name = geometry["name"]
            if len(scan_G0) != len(geometry["G"]):
                logger.debug("#G0 G[] did not match %s", geo_name)
                continue
            if scan_G4 is not None and len(scan_G4) != len(geometry["Q"]):
                logger.debug("#G4 Q[] did not match %s", geo_name)
                continue

            for variant in geometry["variations"]:
                var_name = variant["name"]
                n_motors = len(variant["motors"])
                if scan_positioners[:n_motors] != variant["motors"]:
                    logger.debug("motors did not match %s", geo_name)
                    continue

                others_match = True
                for mne in variant["other-motors"]:
                    if mne not in scan.positioner:
                        others_match = False
                        break
                if not others_match:
                    logger.debug(
                        "other-motors did not match %s (mne=%s)",
                        geo_name,
                        mne,
                    )
                    continue

                match.append("%s.%s" % (geo_name, var_name))

        if len(match) > 1:
            msg = "scan geometry match is not unique!"
            msg += "  Picking the first one from: " + str(match)
            msg += ", file: " + scan.specFile
            msg += ", scan: " + str(scan)
            logger.debug(msg)
        elif len(match) == 0:
            match = [self.get_default_geometry()["name"]]

        return match[0]

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
