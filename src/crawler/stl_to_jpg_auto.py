import os
from stl import mesh
import math
import random
import copy
import time
import glob
import sys

from mpl_toolkits import mplot3d
import matplotlib
from matplotlib import pyplot
from PIL import Image, ImageOps

"""

Generate .jpeg snapshots in rgb and grayscale with
different rotations in order to know the shape of
the .stl model

"""

def write_stl_data_to_img(your_mesh, output_filename):
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten('C')
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.axis('off')
    pyplot.ioff()
    pyplot.savefig(output_filename)

def rgb_to_grayscale(input_filename, output_filename):
    # creating an og_image object
    og_image = Image.open(input_filename)

    # applying grayscale method
    gray_image = ImageOps.grayscale(og_image)
    print(output_filename)
    gray_image.save(output_filename)

def preprocess(stl_filepath, rgb_filepath, grayscale_filepath):
    """
    Given the filepath of a .stl file, read the 3D model, generate one or more rotations and store the result on
    one or more rgb images. Afterwards, convert those images into grayscale images.
    :param stl_filepath:
    :return:
    """
    #filepath = "/".join(stl_filepath.split("/")[:-1])
    filename = stl_filepath.split("/")[-1]
    filename = filename[:-4] # Remove .stl from the filename
    #rgb_filepath = filepath+"/rgb/"
    #grayscale_filepath = filepath+"/grayscale/"

    # Create directories if they don't exist
    if not os.path.exists(rgb_filepath):
        os.makedirs(rgb_filepath)
    if not os.path.exists(grayscale_filepath):
        os.makedirs(grayscale_filepath)

    count=0
    axis = [0.0, 0.0, 0.0]
    #start_load_time = time.time()
    my_mesh = mesh.Mesh.from_file(stl_filepath)
    #end_load_time = time.time()
    #print("Image: {}; Load time: {}s".format(stl_filepath, end_load_time-start_load_time))

    for i in range(len(axis)):
        # Iterates over the axis
        axis = [0.0, 0.0, 0.0]
        axis[i] += 0.5
        for k in range(0,4):
            #for radians in range(0,90,30):
            rgb_filename = filename+"_-_{}.jpeg".format(count)
            radians = random.randint(0,91)
            #my_mesh_copy = copy.copy(my_mesh)
            #start_mutation_time = time.time()
            my_mesh.rotate(axis, math.radians(radians))
            # Apply translation
            x_translation = random.randint(0, 50)
            y_translation = random.randint(0, 50)

            my_mesh.x += x_translation
            my_mesh.y += y_translation
            #end_mutation_time = time.time()
            #print("Time modifications: {}".format(end_mutation_time-start_mutation_time))

            #start_write_time = time.time()
            write_stl_data_to_img(my_mesh, rgb_filepath+rgb_filename)
            #end_write_time = time.time()
            #print("Saving time: {}".format(end_write_time-start_write_time))
            rgb_to_grayscale(rgb_filepath+rgb_filename, grayscale_filepath+rgb_filename)

            # Turn to original
            my_mesh.rotate(axis, -math.radians(radians))
            my_mesh.x -= x_translation
            my_mesh.y -= y_translation
            count += 1



rootPath = "/home/vdasilva@lleidanet.lnst.es/Sergi/InvelonChallenge"

#category_path = "/home/dgl3/InvelonChallenge/data/examples/categories/"
category_path = rootPath + "/data/valid/"

#categories = [name for name in os.listdir(category_path)]

categories = [sys.argv[1]]

for category in categories:
    print(category_path + "/" + category)
    files = glob.glob(category_path + "/" + category + "/*.stl")
    print(f"Files in directory {category_path+category}: {files}")
    for i, file in enumerate(files):
        try:
            print(file, category_path+category+"/rgb/", category_path+category+"/grayscale/")
            preprocess(file, category_path+category+"/rgb/", category_path+category+"/grayscale/")
        except:
            print("error")