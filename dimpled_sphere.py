import os
import FreeCAD, Part
from FreeCAD import Vector
import utils

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

utils.export_to_stl([sphere], stl_file_path)

if 'Gui' in dir(FreeCAD):
    utils.export_to_png(png_file_path)
