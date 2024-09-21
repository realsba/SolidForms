# SolidForms

A collection of FreeCAD Python scripts for constructing geometric figures. Each script generates a 3D model of a specific shape using parametric geometry, allowing for customization and export to STL for 3D printing.

<p float="left">
  <img src="media/SpherifiedCube.png" width="45%" />
  <img src="media/GridCube.png" width="45%" />
</p>

## Features

- **spherified_cube.py**: Generates a cube composed of overlapping hollow spheres, connected by cylinders.
  - Configurable sphere radius, cylinder radius, wall thickness, and cylinder shortening.
- **grid_cube.py**: Generates a grid cube structure made of rods, with spheres at each corner.
  - Customizable cube size and rod radius.  
- Exports directly to STL format for easy 3D printing.
- More shapes and scripts coming soon!

## Dependencies

- **FreeCAD 0.22** (or later)
- Python 3.x

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/SolidForms.git
    ```
2. Open any .py script in FreeCAD's Python console or run it directly from the FreeCAD environment.
3. Modify parameters such as sphere radius, wall thickness, etc., inside the script to customize the model.
4. Export the generated model to STL for 3D printing.

## Example Usage
```bash
python spherified_cube.py
```

This will create a 3x3x3 grid of hollow spheres connected by cylinders. The output is an STL file ready for 3D printing.

## Future Plans
- Add more scripts for different geometric forms.
- Improve the parameterization and customization options for the shapes.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/realsba/SolidForms/blob/main/LICENSE) file for details.

## Author
- Bohdan Sadovyak

## Bugs/Issues
Please report any bugs or issues [here](https://github.com/realsba/SolidForms/issues).