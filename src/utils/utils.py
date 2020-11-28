from stl import mesh
from mpl_toolkits import mplot3d
#import matplotlib
from matplotlib import pyplot
import math
from PIL import Image, ImageOps
#matplotlib.use('Agg')


def write_stl_data_to_img(your_mesh, output_filename):
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten('C')
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.axis('off')
    print(f"Save figure in: {output_filename}")
    pyplot.savefig(output_filename)

def rgb_to_grayscale(input_filename, output_filename):
    # creating an og_image object
    og_image = Image.open(input_filename)

    # applying grayscale method
    gray_image = ImageOps.grayscale(og_image)
    gray_image.save(output_filename)
