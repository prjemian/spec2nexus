
import pprint

with open("geometries.txt", "r") as fp:
    geom = eval(fp.read())

for geo_name, structure in geom.items():
    if "variations" not in structure:
        print(f"{geo_name} {structure['numgeo']} {structure['variants']}")
        variations = dict(standard={'motors': [], 'other-motors': []})
        structure['variations'] = variations
        if not structure['variants']:
            variations['standard']['motors'] = structure["motors"]
            del structure["motors"]
    else:
        print(f"{geo_name} {structure['numgeo']} {len(structure['variations'])}")

pprint.pprint(geom, indent=2)
