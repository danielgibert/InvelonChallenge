import numpy
from stl import mesh

my_mesh = mesh.Mesh.from_file('../../data/examples/Ender+3+Bed+Level/files/Bed_Levelling_Ender_3.stl')

print(my_mesh.normals)