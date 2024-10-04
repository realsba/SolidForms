import FreeCAD

def export_to_png(png_file_path):
    FreeCAD.ActiveDocument.recompute()
    view = FreeCAD.Gui.activeDocument().activeView()
    view.viewIsometric()
    view.fitAll()
    view.saveImage(png_file_path, 1000, 1000, "")
    print(f"Exported to {png_file_path}")
