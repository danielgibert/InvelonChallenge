import os
from stl import mesh
import math
import sys
sys.path.append("../../")
from src.utils.utils import write_stl_data_to_img, rgb_to_grayscale
import random
import copy
import time

def preprocess_v2(stl_filepath, rgb_filepath, grayscale_filepath):
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
            rgb_filename = filename+"{}.jpeg".format(count)
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

def preprocess(stl_filepath):
    """
    Given the filepath of a .stl file, read the 3D model, generate one or more rotations and store the result on
    one or more rgb images. Afterwards, convert those images into grayscale images.
    :param stl_filepath:
    :return:
    """
    filepath = "/".join(stl_filepath.split("/")[:-1])
    filename = stl_filepath.split("/")[-1]
    filename = filename[:-4] # Remove .stl from the filename
    rgb_filepath = filepath+"/rgb/"
    grayscale_filepath = filepath+"/grayscale/"

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
            rgb_filename = filename+"{}.jpeg".format(count)
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

    # ToDo Object translation
    # Translate 2 points over the X axis
    # my_mesh.x += 2

    # Rotate 90 degrees over the X axis
    # my_mesh.rotate([0.5, 0.0, 0.0], math.radians(90))
    # Translate 2 points over the X and Y points
    # my_mesh.x += 2
    # my_mesh.y += 2
#preprocess('../../data/examples/Ender+3+Bed+Level/files/Bed_Levelling_Ender_3.stl', '../../data/examples/Ender+3+Bed+Level/files/rgb', '../../data/examples/Ender+3+Bed+Level/files/grayscale')

#preprocess('../../data/examples/Ender+3+Bed+Level/files/Bed_Levelling_Ender_3.stl')
#preprocess('../../data/examples/Psyduck(Pokemon)/files/Psyduck.stl')

