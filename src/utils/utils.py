from mpl_toolkits import mplot3d
from matplotlib import pyplot
from PIL import Image, ImageOps


def write_stl_data_to_img(your_mesh, output_filename):
    """
    Writes .stl data to RGB image using mplot3d
    :param your_mesh: mesh
    :param output_filename: str
    :return: None
    """
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten('C')
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.axis('off')
    pyplot.savefig(output_filename)

def rgb_to_grayscale(input_filename, output_filename):
    """
    Writes RGB image into grayscale
    :param input_filename: str
    :param output_filename: str
    :return: None
    """
    # creating an og_image object
    og_image = Image.open(input_filename)

    # applying grayscale method
    gray_image = ImageOps.grayscale(og_image)
    gray_image.save(output_filename)
