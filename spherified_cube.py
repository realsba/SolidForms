import os
import FreeCAD, Part, Mesh, MeshPart

# Parameters
sphere_radius = 10              # Outer radius of spheres
cylinder_radius = 1             # Radius of cylinders
wall_thickness = 0.75           # Thickness of the hollow sphere walls
overlap_radius = 0.1            # Additional radius for sphere overlap
cylinder_shorten = 0.25         # Shortening length for cylinders (from both ends)
distance = sphere_radius * 2    # Distance between sphere centers
dimension = 3                   # Default dimension (3x3x3)
cube_size = distance * dimension # Size of the cube

# Export paths
stl_file_path = os.path.expanduser("~/SpherifiedCube.stl")
svg_file_path = os.path.expanduser("~/SpherifiedCube.svg")

doc = FreeCAD.ActiveDocument
mesh = Mesh.Mesh()

for x in range(dimension):
    for y in range(dimension):
        for z in range(dimension):
            sphere_center = FreeCAD.Vector(
                x * distance + sphere_radius,
                y * distance + sphere_radius,
                z * distance + sphere_radius
            )
            # Create outer and inner spheres with overlap
            outer_sphere = Part.makeSphere(sphere_radius + overlap_radius, sphere_center)
            inner_sphere = Part.makeSphere(sphere_radius + overlap_radius - wall_thickness, sphere_center)
            # Subtract the inner sphere from the outer one to make it hollow
            hollow_sphere = outer_sphere.cut(inner_sphere)
            Part.show(hollow_sphere)
            hollow_sphere_mesh = MeshPart.meshFromShape(Shape=hollow_sphere, LinearDeflection=0.1, AngularDeflection=0.1)
            mesh.addMesh(hollow_sphere_mesh)

# Create cylinders from unique points on three faces of the cube
for x in range(dimension):
    for y in range(dimension):
        # Bottom face (z = 0), adjust start point and length
        point_bottom = FreeCAD.Vector(
            x * distance + sphere_radius,
            y * distance + sphere_radius,
            cylinder_shorten  # Shift the start point up
        )
        cylinder_bottom = Part.makeCylinder(cylinder_radius, cube_size - 2 * cylinder_shorten, point_bottom, FreeCAD.Vector(0, 0, 1))
        Part.show(cylinder_bottom)
        cylinder_bottom_mesh = MeshPart.meshFromShape(Shape=cylinder_bottom, LinearDeflection=0.1, AngularDeflection=0.1)
        mesh.addMesh(cylinder_bottom_mesh)

        # Front face (y = 0), adjust start point and length
        point_front = FreeCAD.Vector(
            x * distance + sphere_radius,
            cylinder_shorten,  # Shift the start point forward
            y * distance + sphere_radius
        )
        cylinder_front = Part.makeCylinder(cylinder_radius, cube_size - 2 * cylinder_shorten, point_front, FreeCAD.Vector(0, 1, 0))
        Part.show(cylinder_front)
        cylinder_front_mesh = MeshPart.meshFromShape(Shape=cylinder_front, LinearDeflection=0.1, AngularDeflection=0.1)
        mesh.addMesh(cylinder_front_mesh)

        # Left face (x = 0), adjust start point and length
        point_left = FreeCAD.Vector(
            cylinder_shorten,  # Shift the start point to the right
            x * distance + sphere_radius,
            y * distance + sphere_radius
        )
        cylinder_left = Part.makeCylinder(cylinder_radius, cube_size - 2 * cylinder_shorten, point_left, FreeCAD.Vector(1, 0, 0))
        Part.show(cylinder_left)
        cylinder_left_mesh = MeshPart.meshFromShape(Shape=cylinder_left, LinearDeflection=0.1, AngularDeflection=0.1)
        mesh.addMesh(cylinder_left_mesh)

# Save the mesh to STL file
mesh.write(stl_file_path)

# Check that export was successful
print(f"Exported to {stl_file_path}")

# Recompute the document to update the view
FreeCAD.ActiveDocument.recompute()
