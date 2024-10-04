import os
import FreeCAD, Part
from FreeCAD import Vector
import utils

sphere_radius = 25
cylinder_radius = 12
wall_thickness = 1

outer_sphere = Part.makeSphere(sphere_radius)
inner_sphere = Part.makeSphere(sphere_radius - wall_thickness)
sphere = outer_sphere.cut(inner_sphere)

stl_file_path = os.path.expanduser("~/Sphere1.stl")
png_file_path = os.path.expanduser("~/Sphere1.png")

vectors = [Vector(x, y, z).normalize() for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]

holes = []
for vec in vectors:
    cylinder = Part.makeCylinder(cylinder_radius, sphere_radius , -vec * sphere_radius, vec)
    sphere = sphere.fuse(cylinder)
    hole = Part.makeCylinder(cylinder_radius - wall_thickness, sphere_radius, -vec * sphere_radius, vec)
    holes.append(hole)

for hole in holes:
    sphere = sphere.cut(hole)

sphere = sphere.common(outer_sphere)

Part.show(sphere)

utils.export_to_stl([sphere], stl_file_path)

if 'Gui' in dir(FreeCAD):
    utils.export_to_png(png_file_path)
