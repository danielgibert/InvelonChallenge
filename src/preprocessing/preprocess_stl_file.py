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
    :param stl_filepath: str
    :param rgb_filepath: str
    :param grayscale_filepath: str
    :return: None
    """
    filename = stl_filepath.split("/")[-1]
    filename = filename[:-4] # Remove .stl from the filename

    # Create directories if they don't exist
    if not os.path.exists(rgb_filepath):
        os.makedirs(rgb_filepath)
    if not os.path.exists(grayscale_filepath):
        os.makedirs(grayscale_filepath)

    count=0
    axis = [0.0, 0.0, 0.0]
    my_mesh = mesh.Mesh.from_file(stl_filepath)

    for i in range(len(axis)):
        # Iterates over the axis
        axis = [0.0, 0.0, 0.0]
        axis[i] += 0.5
        for k in range(0,4):
            rgb_filename = filename+"{}.jpeg".format(count)
            radians = random.randint(0,91)
            #my_mesh_copy = copy.copy(my_mesh)

            my_mesh.rotate(axis, math.radians(radians))
            # Apply translation
            x_translation = random.randint(0, 50)
            y_translation = random.randint(0, 50)

            my_mesh.x += x_translation
            my_mesh.y += y_translation

            write_stl_data_to_img(my_mesh, rgb_filepath+rgb_filename)
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
    :param stl_filepath: str
    :return: None
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
    my_mesh = mesh.Mesh.from_file(stl_filepath)

    for i in range(len(axis)):
        # Iterates over the axis
        axis = [0.0, 0.0, 0.0]
        axis[i] += 0.5
        for k in range(0,4):
            rgb_filename = filename+"{}.jpeg".format(count)
            radians = random.randint(0,91)
            #my_mesh_copy = copy.copy(my_mesh)
            my_mesh.rotate(axis, math.radians(radians))
            # Apply translation
            x_translation = random.randint(0, 50)
            y_translation = random.randint(0, 50)

            my_mesh.x += x_translation
            my_mesh.y += y_translation

            write_stl_data_to_img(my_mesh, rgb_filepath+rgb_filename)
            rgb_to_grayscale(rgb_filepath+rgb_filename, grayscale_filepath+rgb_filename)

            # Turn to original
            my_mesh.rotate(axis, -math.radians(radians))
            my_mesh.x -= x_translation
            my_mesh.y -= y_translation
            count += 1
