import FreeCAD, Part

def export_to_svg(shape, file_path):
    # Create a new document for SVG export
    svg_doc = FreeCAD.newDocument("SVG_Export")

    # Create a feature for the shape
    feature = svg_doc.addObject("Part::Feature", "Shape")
    feature.Shape = shape

    # Export the document as SVG
    FreeCADGui.activeDocument().export(file_path)

    print(f"Exported to {file_path}")
