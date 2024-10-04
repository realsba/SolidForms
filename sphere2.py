import os
import FreeCAD
import Part, Mesh, MeshPart
from FreeCAD import Vector
from utils import export_to_png

sphere_radius = 20
cylinder_radius = 9
wall_thickness = 1

outer_sphere = Part.makeSphere(sphere_radius)
inner_sphere = Part.makeSphere(sphere_radius - wall_thickness)
sphere = outer_sphere.cut(inner_sphere)

stl_file_path = os.path.expanduser("~/Sphere2.stl")
png_file_path = os.path.expanduser("~/Sphere2.png")


holes = []

vectors = [
    Vector(1, 1, 0).normalize(),
    Vector(-1, 1, 0).normalize(),
    Vector(1, -1, 0).normalize(),
    Vector(-1, -1, 0).normalize(),

    Vector(1, 0, 1).normalize(),
    Vector(-1, 0, 1).normalize(),
    Vector(1, 0, -1).normalize(),
    Vector(-1, 0, -1).normalize(),

    Vector(0, 1, 1).normalize(),
    Vector(0, -1, 1).normalize(),
    Vector(0, 1, -1).normalize(),
    Vector(0, -1, -1).normalize(),
]

for vec in vectors:
    cylinder = Part.makeCylinder(cylinder_radius, sphere_radius * 2, -vec * sphere_radius, vec)
    sphere = sphere.fuse(cylinder)
    hole = Part.makeCylinder(cylinder_radius - wall_thickness, sphere_radius * 2, -vec * sphere_radius, vec)
    holes.append(hole)

sphere = sphere.common(outer_sphere)

for hole in holes:
    sphere = sphere.cut(hole)

Part.show(sphere)

mesh = Mesh.Mesh()
mesh.addMesh(MeshPart.meshFromShape(Shape=sphere, LinearDeflection=0.1, AngularDeflection=0.1))
mesh.write(stl_file_path)

if 'Gui' in dir(FreeCAD):
    export_to_png(png_file_path)
