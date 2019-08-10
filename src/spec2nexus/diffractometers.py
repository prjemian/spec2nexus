#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2019, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
Describe SPEC #G control lines

  #G0 ...          geometry parameters from G[] array (geo mode, sector, etc)
  #G1 ...          geometry parameters from U[] array (lattice constants, orientation reflections)
  #            G2 is unused
  #G3 ...          geometry parameters from UB[] array (orientation matrix)
  #G4 ...          geometry parameters from Q[] array (lambda, frozen angles, cut points, etc)

"""

import logging
import os


logger = logging.getLogger(__name__)
_path = os.path.dirname(__file__)
DICT_FILE = os.path.join(_path, "diffractometer-geometries.dict")


class DiffractometerGeometryCatalog:
    """
    catalog of the diffractometer geometries known to SPEC
    """
    
    db = {}
    
    def __init__(self):
        with open(DICT_FILE, "r") as fp:
            self.db = eval(fp.read())
        
        self._default_geometry = list(self.db.values())[0]
    
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
        result = []
        for nm, geometry in self.db.items():
            if variations:
                result += ["%s.%s" % (nm, s) for s in geometry["variations"].keys()]
            else:
                result.append(nm)
        return result
    
    def _split_name_variation_(self, geo_name):
        """
        split geo_name into geometry name and variation
        """
        nm = geo_name
        try:
            nm, variant = geo_name.split(".")
        except ValueError:
            variant = None
        return nm, variant
    
    def get(self, geo_name, default=None):
        """
        return dictionary for diffractometer geometry ``geo_name``
        """
        nm = self._split_name_variation_(geo_name)[0]
        return self.db.get(nm, default)
    
    def get_default_geometry(self):
        " "
        return self._default_geometry
    
    def hasGeometry(self, geo_name):
        """
        Is the ``geo_name`` geometry defined?  True or False
        """
        nm, variant = self._split_name_variation_(geo_name)
        if variant is None:
            return nm in self.db
        else:
            return variant in self.db[nm]["variations"]
    
    def _get_scan_positioners_(self, scan):
        scan_positioners = []
        if hasattr(scan.header, 'o'):       # prefer mnemonics
            for row in scan.header.o:
                scan_positioners += row
        elif hasattr(scan.header, 'O'):
            for row in scan.header.O:
                scan_positioners += [k.lower() for k in row]
        else:
            scan_positioners = [k.lower() for k in scan.positioner.keys()]
        if len(scan_positioners) > 0:
            scan_positioners_new = []
            for k in scan_positioners:
                if k in ("delta",):
                    k = "del"
                elif k in ("theta",):
                    k = "th"
                elif k in ("2-theta", "two theta") or k.endswith("tth"):
                    k = "tth"
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

        try:
            scan_G0 = scan.G['G0'].split()
            scan_G4 = scan.G['G4'].split()
        except KeyError:
            scan_G0, scan_G4 = [], []
        if scan_G0 == ['0',] and  scan_G4 == ['0',]:
            # no_hkl case
            scan_G0, scan_G4 = [], []

        for geo_name, geometry in self.db.items():
            if len(scan_G0) != len(geometry["G"]):
                continue
            if len(scan_G4) != len(geometry["Q"]):
                continue
            
            for var_name, variant in geometry["variations"].items():
                n_motors = len(variant["motors"])
                if scan_positioners[:n_motors] != variant["motors"]:
                    continue

                others_match = True
                for mne in variant["other-motors"]:
                    if mne not in scan.positioner:
                        others_match = False
                        break
                if not others_match:
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