import os
import FreeCAD, Part
import utils

# Parameters
sphere_radius = 15              # Outer radius of spheres
rod_radius = 1.5
reinforcement_radius = 5
wall_thickness = 0.8            # Thickness of the hollow sphere walls
overlap_radius = 0.1            # Additional radius for sphere overlap
distance = sphere_radius * 2    # Distance between sphere centers
dimension = 2
cube_size = distance * dimension

# Export paths
stl_file_path = os.path.expanduser("~/SpherifiedCube.stl")
png_file_path = os.path.expanduser("~/SpherifiedCube.png")


def create_hollow_sphere(radius, center, wall_thickness):
    """Create a hollow sphere at the given center."""
    outer_sphere = Part.makeSphere(radius, center)
    inner_sphere = Part.makeSphere(radius - wall_thickness, center)
    return outer_sphere.cut(inner_sphere)


def create_rod(radius, height, point, direction, wall_thickness):
    """Create a rod at the given point in the specified direction."""
    outer_cylinder = Part.makeCylinder(radius, height, point, direction)
    inner_cylinder = Part.makeCylinder(radius - wall_thickness, height, point, direction)
    reinforcement_sphere1 = create_hollow_sphere(reinforcement_radius, point, wall_thickness)
    end_point = point + direction.normalize() * height
    reinforcement_sphere2 = create_hollow_sphere(reinforcement_radius, end_point, wall_thickness)
    return outer_cylinder.cut(inner_cylinder).fuse(reinforcement_sphere1).fuse(reinforcement_sphere2)


def create_structure():
    shapes = []
    sphere_centers = []

    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                sphere_center = FreeCAD.Vector(
                    x * distance + sphere_radius,
                    y * distance + sphere_radius,
                    z * distance + sphere_radius
                )
                sphere_centers.append(sphere_center)

    for sphere_center in sphere_centers:
        hollow_sphere = create_hollow_sphere(sphere_radius + overlap_radius, sphere_center, wall_thickness)
        reinforcement_sphere = create_hollow_sphere(reinforcement_radius, sphere_center, wall_thickness)
        combined_sphere = hollow_sphere.fuse(reinforcement_sphere)

        Part.show(reinforcement_sphere)
        Part.show(combined_sphere)
        shapes.append(combined_sphere)

    # Directions for rods and corresponding positions using tuples as keys
    directions = [
        (0, 0, 1),  # Z direction (bottom face)
        (0, 1, 0),  # Y direction (front face)
        (1, 0, 0)  # X direction (left face)
    ]

    positions = {
        (0, 0, 1): lambda i, j: FreeCAD.Vector(i * distance + sphere_radius, j * distance + sphere_radius, 0),
        (0, 1, 0): lambda i, j: FreeCAD.Vector(i * distance + sphere_radius, 0, j * distance + sphere_radius),
        (1, 0, 0): lambda i, j: FreeCAD.Vector(0, i * distance + sphere_radius, j * distance + sphere_radius),
    }

    for i in range(dimension):
        for j in range(dimension):
            for d in directions:
                point = positions[d](i, j)
                rod = create_rod(rod_radius, cube_size, point, FreeCAD.Vector(*d), wall_thickness)

                start_point = point + FreeCAD.Vector(*d).normalize() * sphere_radius
                end_point = point + FreeCAD.Vector(*d).normalize() * (cube_size - sphere_radius)
                solid_sphere1 = Part.makeSphere(sphere_radius, start_point)
                solid_sphere2 = Part.makeSphere(sphere_radius, end_point)
                cylinder_length = (end_point - start_point).Length
                solid_cylinder = Part.makeCylinder(sphere_radius, cylinder_length, start_point,
                                                   FreeCAD.Vector(*d).normalize())
                shape = solid_sphere1.fuse(solid_sphere2).fuse(solid_cylinder)

                rod = rod.common(shape)

                Part.show(rod)
                shapes.append(rod)

    return shapes


# Main execution
shapes = create_structure()

utils.export_to_stl(shapes, stl_file_path)

if 'Gui' in dir(FreeCAD):
    utils.export_to_png(png_file_path)
