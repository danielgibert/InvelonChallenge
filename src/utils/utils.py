from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def plot_mesh_stl_file(stl_filename):
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file(stl_filename)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten('C')
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()

plot_mesh_stl_file('../../data/examples/Ender+3+Bed+Level/files/Bed_Levelling_Ender_3.stl')