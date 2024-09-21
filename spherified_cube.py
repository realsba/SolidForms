import os
import FreeCAD, Part, Mesh, MeshPart

# Parameters
sphere_radius = 10              # Outer radius of spheres
cylinder_radius = 1
wall_thickness = 0.75           # Thickness of the hollow sphere walls
overlap_radius = 0.1            # Additional radius for sphere overlap
cylinder_shorten = 0.25         # Shortening length for cylinders (from both ends)
distance = sphere_radius * 2    # Distance between sphere centers
dimension = 3                   # Default dimension (3x3x3)
cube_size = distance * dimension

# Export paths
stl_file_path = os.path.expanduser("~/SpherifiedCube.stl")
png_file_path = os.path.expanduser("~/SpherifiedCube.png")

doc = FreeCAD.ActiveDocument

def create_structure():
    shapes = []  # Store both hollow spheres and cylinders for later SVG export
    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                sphere_center = FreeCAD.Vector(
                    x * distance + sphere_radius,
                    y * distance + sphere_radius,
                    z * distance + sphere_radius
                )
                outer_sphere = Part.makeSphere(sphere_radius + overlap_radius, sphere_center)
                inner_sphere = Part.makeSphere(sphere_radius + overlap_radius - wall_thickness, sphere_center)
                hollow_sphere = outer_sphere.cut(inner_sphere)
                Part.show(hollow_sphere)
                shapes.append(hollow_sphere)

    for x in range(dimension):
        for y in range(dimension):
            # Bottom face (z = 0)
            point_bottom = FreeCAD.Vector(x * distance + sphere_radius, y * distance + sphere_radius, cylinder_shorten)
            cylinder_bottom = Part.makeCylinder(cylinder_radius, cube_size - 2 * cylinder_shorten, point_bottom, FreeCAD.Vector(0, 0, 1))
            Part.show(cylinder_bottom)
            shapes.append(cylinder_bottom)

            # Front face (y = 0)
            point_front = FreeCAD.Vector(x * distance + sphere_radius, cylinder_shorten, y * distance + sphere_radius)
            cylinder_front = Part.makeCylinder(cylinder_radius, cube_size - 2 * cylinder_shorten, point_front, FreeCAD.Vector(0, 1, 0))
            Part.show(cylinder_front)
            shapes.append(cylinder_front)

            # Left face (x = 0)
            point_left = FreeCAD.Vector(cylinder_shorten, x * distance + sphere_radius, y * distance + sphere_radius)
            cylinder_left = Part.makeCylinder(cylinder_radius, cube_size - 2 * cylinder_shorten, point_left, FreeCAD.Vector(1, 0, 0))
            Part.show(cylinder_left)
            shapes.append(cylinder_left)

    return shapes

def export_to_stl(shapes):
    mesh = Mesh.Mesh()
    for shape in shapes:
        mesh.addMesh(MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.1))
    mesh.write(stl_file_path)
    print(f"Exported to {stl_file_path}")

def show_isometric_view():
    FreeCAD.ActiveDocument.recompute()
    view = FreeCAD.Gui.activeDocument().activeView()
    view.viewIsometric()
    view.fitAll()
    FreeCAD.Gui.updateGui()

def export_to_png(file_path):
    # Set the view for rendering
    view = FreeCAD.Gui.activeDocument().activeView()
    view.saveImage(file_path, 1000, 1000, "")
    print(f"Exported to {file_path}")

# Main execution
shapes = create_structure()

export_to_stl(shapes)

show_isometric_view()

export_to_png(png_file_path)
