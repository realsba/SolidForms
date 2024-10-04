import os
import FreeCAD
import Part, Mesh, MeshPart
from FreeCAD import Vector
from utils import export_to_png

sphere_radius = 25
small_sphere_radius = 14
wall_thickness = 1

stl_file_path = os.path.expanduser("~/DimpledSphere.stl")
png_file_path = os.path.expanduser("~/DimpledSphere.png")

outer_sphere = Part.makeSphere(sphere_radius)
inner_sphere = Part.makeSphere(sphere_radius - wall_thickness)
sphere = outer_sphere.cut(inner_sphere)

vectors = [
    Vector(x, y, z).normalize().multiply(sphere_radius)
    for x in (-1, 1)
    for y in (-1, 1)
    for z in (-1, 1)
]

small_sphere = Part.makeSphere(small_sphere_radius)
inner_small_sphere = Part.makeSphere(small_sphere_radius - wall_thickness)
for vec in vectors:
    small_sphere.Placement.Base = vec
    inner_small_sphere.Placement.Base = vec
    sphere = sphere.fuse(small_sphere).cut(inner_small_sphere)

sphere = sphere.common(outer_sphere)
Part.show(sphere)

mesh = Mesh.Mesh()
mesh.addMesh(MeshPart.meshFromShape(Shape=sphere, LinearDeflection=0.1, AngularDeflection=0.1))
mesh.write(stl_file_path)
print(f"STL exported to {stl_file_path}")

if 'Gui' in dir(FreeCAD):
    export_to_png(png_file_path)
