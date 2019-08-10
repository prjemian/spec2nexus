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

import os

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
        s = f"DiffractometerGeometryCatalog(number={len(self.db)})"
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
                result += [f"{nm}.{s}" for s in geometry["variations"].keys()]
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
        return self._default_geometry
    
    def hasGeometry(self, geo_name):
        """
        is the ``geo_name`` geometry defined?
        """
        nm, variant = self._split_name_variation_(geo_name)
        if variant is None:
            return nm in self.db
        else:
            return variant in self.db[nm]["variations"]
    
    def match(self, scan):
        """
        find the ``geo_name`` geometry that matches the ``scan``
        """
        match = []
        scan_positioners = [k.lower() for k in scan.positioner.keys()]
        if len(scan_positioners) > 0 and scan_positioners[0] == "2-theta":
            scan_positioners[0] = 'tth'
        try:
            scan_G0 = scan.G['G0'].split()
            scan_G4 = scan.G['G4'].split()
        except KeyError:
            scan_G0, scan_G4 = [], []
        if scan_G0 == ['0',] and  scan_G4 == ['0',]:
            # no_hkl case
            scan_G0, scan_G4 = [], []
        for geo_name, geometry in self.db.items():
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
                # match length of scan's #G0 line
                if len(scan_G0) != len(geometry["G"]):
                    continue
                # match length of scan's #G4 line
                if len(scan_G4) != len(geometry["Q"]):
                    continue
                match.append(f"{geo_name}.{var_name}")
        # if len(match) > 1:
        #     print(f"file: {scan.specFile}")
        #     print(f"scan: {scan}")
        #     print(f"scan geometry match is not unique! {match}")
        #     print("picking the first one")
        if len(match) == 0:
            match = [self._default_geometry["name"]]
        return match[0]
