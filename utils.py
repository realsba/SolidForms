import FreeCAD, Mesh, MeshPart

def export_to_png(png_file_path):
    FreeCAD.ActiveDocument.recompute()
    view = FreeCAD.Gui.activeDocument().activeView()
    view.viewIsometric()
    view.fitAll()
    view.saveImage(png_file_path, 1000, 1000, "")
    print(f"Exported to {png_file_path}")

def export_to_stl(shapes, stl_file_path):
    mesh = Mesh.Mesh()
    for shape in shapes:
        mesh.addMesh(MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.1))
    mesh.write(stl_file_path)
    print(f"Exported to {stl_file_path}")
