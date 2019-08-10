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


def main():
    with open("diffractometer-geometries.dict", "r") as fp:
        geom = eval(fp.read())

    for geo_name, structure in geom.items():
#         diffractometer = Diffractometer(geo_name)
#         diffractometer.geometry = [Term(*t) for t in structure["G"]]
#         diffractometer.constraints = [Term(*t) for t in structure["Q"]]
#         diffractometer.modes = structure["modes"]
#         diffractometer.variations = [
#             DiffractometerVariation(k, v["motors"], v["other-motors"])
#             for k, v in structure["variations"].items()
#             ]
        
        print(f"class {geo_name.title()}Diffractometer(Diffractometer):")
        print("    \"\"\"")
        print(f"    diffractometer/spectrometer with {geo_name} geometry")
        print("    \"\"\"")
        print()
        print(f"    def __init__(self, name):")
        print(f"        self.geometry_name = '{geo_name}'")
        print("        super().__init__(name)")
        print()
        print("        # different combinations of required motors")
        print(f"        self.variations = []")
        for var, spec in structure["variations"].items():
            if len(spec['other-motors']) == 0:
                if len(spec['motors']) == 0:
                    s = f"DiffractometerVariation('{var}')"
                else:
                    s = f"DiffractometerVariation('{var}', {spec['motors']})"
            else:
                s = f"DiffractometerVariation('{var}', {spec['motors']}, {spec['other-motors']})"
            print(f"        self.variations.append({s})")
        print()
        print("        # Strings describing geometry modes")
        print(f"        self.modes = {structure['modes']}")
        print()
        print("        #G0 geometry parameters from G[] array (geo mode, sector, etc)")
        print(f"        self.geometry = []")
        for t in structure["G"]:
            print(f"        self.geometry.append(Term{t})")
        print()
        print("        #G4 geometry parameters from Q[] array (lambda, frozen angles, cut points, etc)")
        print(f"        self.constraints = []")
        for t in structure["Q"]:
            print(f"        self.constraints.append(Term{t})")
        print()
        print()


if __name__ == "__main__":
    main()
