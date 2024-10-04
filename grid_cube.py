import os
import FreeCAD, Part
import utils

# Parameters
size = 30                       # Cube size in mm
step = 10                       # Step size in mm
rodRadius = 1.4                 # Radius of the rods in mm
sphereRadius = rodRadius        # Radius of the spheres

# Export paths
stl_file_path = os.path.expanduser("~/GridCube.stl")
png_file_path = os.path.expanduser("~/GridCube.png")

doc = FreeCAD.ActiveDocument

def create_structure():
    shapes = []

    # Create rods perpendicular to the XY plane
    for x in range(0, size + step, step):
        for y in range(0, size + step, step):
            rod = Part.makeCylinder(rodRadius, size, FreeCAD.Vector(x, y, 0), FreeCAD.Vector(0, 0, 1))
            Part.show(rod)
            shapes.append(rod)

    # Create rods perpendicular to the XZ plane
    for x in range(0, size + step, step):
        for z in range(0, size + step, step):
            rod = Part.makeCylinder(rodRadius, size, FreeCAD.Vector(x, 0, z), FreeCAD.Vector(0, 1, 0))
            Part.show(rod)
            shapes.append(rod)

    # Create rods perpendicular to the YZ plane
    for y in range(0, size + step, step):
        for z in range(0, size + step, step):
            rod = Part.makeCylinder(rodRadius, size, FreeCAD.Vector(0, y, z), FreeCAD.Vector(1, 0, 0))
            Part.show(rod)
            shapes.append(rod)

    # Create spheres at the corners of the cube
    corners = [
        (0, 0, 0),
        (0, size, 0),
        (size, 0, 0),
        (size, size, 0),
        (0, 0, size),
        (0, size, size),
        (size, 0, size),
        (size, size, size)
    ]
    for corner in corners:
        sphere = Part.makeSphere(sphereRadius, FreeCAD.Vector(*corner))
        Part.show(sphere)
        shapes.append(sphere)

    return shapes

# Main execution
shapes = create_structure()

utils.export_to_stl(shapes, stl_file_path)

if 'Gui' in dir(FreeCAD):
    utils.export_to_png(png_file_path)
