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


DICT_FILE = "diffractometer-geometries.dict"

from collections import namedtuple


Term = namedtuple('Term', 'var description')


class Diffractometer:
    """
    Describe a diffractometer in SPEC
    """
    
    def __init__(self, name):
        self.geometry_name = None
        self.name = name
        self.variations = {}
        self.modes = []
        self.geometry = []          # G[], #G0
        self.constraints = []       # A[], #G4



class DiffractometerVariation:
    """
    lists of motors (mnemonics) that describe a diffractometer variation in SPEC
    """
    
    def __init__(self, name, motors=[], others=[]):
        self.name = name
        self.first_motors = motors      # required to come first, in order
        self.additional_motors = others # required to be defined


class DiffractometerGeometryCatalog:
    """
    catalog of the diffractometer geometries known to SPEC
    """
    
    db = {}
    
    def __init__(self):
        with open(DICT_FILE, "r") as fp:
            self.db = eval(fp.read())
    
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
    
    def get(self, geo_name, default=None):
        """
        return dictionary for diffractometer geometry ``geo_name``
        """
        return self.db.get(geo_name, default)
    
    def hasGeometry(self, geo_name):
        """
        is the ``geo_name`` geometry defined?
        """
        try:
            nm, variant = geo_name.split(".")
            if nm in self.db:
                return variant in self.db[nm]["variations"]
            else:
                return False
        except ValueError:
            return geo_name in self.db
    
    def match(self, scan):
        """
        find the ``geo_name`` geometry that matches the ``scan``
        """
        match = None
        for geo_name, geometry in self.db.items():
            pass


def main():
    dgc = DiffractometerGeometryCatalog()
    # print("\n".join(dgc.geometries()))
    # print("\n".join(dgc.geometries(True)))
    for key in "fourc fivec sixc fourc.kappa fivec.kappa sixc.kappa".split():
        print(key, dgc.hasGeometry(key))


if __name__ == "__main__":
    main()
