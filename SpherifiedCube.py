import FreeCAD, Part, Mesh, MeshPart

# Parameters
sphereRadius = 5                # Outer radius of spheres
cylinderRadius = 1              # Radius of cylinders
wallThickness = 0.75            # Thickness of the hollow sphere walls
overlapRadius = 0.1             # Additional radius for sphere overlap
cylinderShorten = 0.25          # Shortening length for cylinders (from both ends)
distance = sphereRadius * 2     # Distance between sphere centers
dimension = 3                   # Default dimension (3x3x3)
stlFilePath = "/home/sba/model.stl"

doc = FreeCAD.ActiveDocument
mesh = Mesh.Mesh()

for x in range(dimension):
    for y in range(dimension):
        for z in range(dimension):
            sphereCenter = FreeCAD.Vector(
                x * distance + sphereRadius,
                y * distance + sphereRadius,
                z * distance + sphereRadius
            )
            # Create outer and inner spheres with overlap
            outerSphere = Part.makeSphere(sphereRadius + overlapRadius, sphereCenter)
            innerSphere = Part.makeSphere(sphereRadius + overlapRadius - wallThickness, sphereCenter)
            # Subtract the inner sphere from the outer one to make it hollow
            hollowSphere = outerSphere.cut(innerSphere)
            Part.show(hollowSphere)
            hollowSphereMesh = MeshPart.meshFromShape(Shape=hollowSphere, LinearDeflection=0.1, AngularDeflection=0.1)
            mesh.addMesh(hollowSphereMesh)

cubeSize = distance * dimension  # Size of the cube

# Create cylinders from unique points on three faces of the cube
for x in range(dimension):
    for y in range(dimension):
        # Bottom face (z = 0), adjust start point and length
        pointBottom = FreeCAD.Vector(
            x * distance + sphereRadius,
            y * distance + sphereRadius,
            cylinderShorten  # Shift the start point up
        )
        cylinderBottom = Part.makeCylinder(cylinderRadius, cubeSize - 2 * cylinderShorten, pointBottom, FreeCAD.Vector(0, 0, 1))
        Part.show(cylinderBottom)
        cylinderBottomMesh = MeshPart.meshFromShape(Shape=cylinderBottom, LinearDeflection=0.1, AngularDeflection=0.1)
        mesh.addMesh(cylinderBottomMesh)

        # Front face (y = 0), adjust start point and length
        pointFront = FreeCAD.Vector(
            x * distance + sphereRadius,
            cylinderShorten,  # Shift the start point forward
            y * distance + sphereRadius
        )
        cylinderFront = Part.makeCylinder(cylinderRadius, cubeSize - 2 * cylinderShorten, pointFront, FreeCAD.Vector(0, 1, 0))
        Part.show(cylinderFront)
        cylinderFrontMesh = MeshPart.meshFromShape(Shape=cylinderFront, LinearDeflection=0.1, AngularDeflection=0.1)
        mesh.addMesh(cylinderFrontMesh)

        # Left face (x = 0), adjust start point and length
        pointLeft = FreeCAD.Vector(
            cylinderShorten,  # Shift the start point to the right
            x * distance + sphereRadius,
            y * distance + sphereRadius
        )
        cylinderLeft = Part.makeCylinder(cylinderRadius, cubeSize - 2 * cylinderShorten, pointLeft, FreeCAD.Vector(1, 0, 0))
        Part.show(cylinderLeft)
        cylinderLeftMesh = MeshPart.meshFromShape(Shape=cylinderLeft, LinearDeflection=0.1, AngularDeflection=0.1)
        mesh.addMesh(cylinderLeftMesh)

# Save the mesh to STL file
mesh.write(stlFilePath)

# Check that export was successful
print(f"Exported to {stlFilePath}")

# Recompute the document to update the view
FreeCAD.ActiveDocument.recompute()
