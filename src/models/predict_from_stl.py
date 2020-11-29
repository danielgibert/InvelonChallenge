import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
from stl import mesh
import random
import math
import sys
sys.path.append("../../")
from src.utils.utils import write_stl_data_to_img, rgb_to_grayscale
import shutil


def predict(model_filepath, stl_filepath, width=480, height=640):
    reconstructed_model = keras.models.load_model(model_filepath)
    predictions_list = []
    filename = stl_filepath.split("/")[-1]
    filename = filename[:-4]

    filepath = "/".join(stl_filepath.split("/"))[:-1]
    rgb_filepath = filepath+"/tmp_rgb/"
    grayscale_filepath = filepath+"/tmp_grayscale/"
    # Create temporal directories directories if they don't exist
    if not os.path.exists(rgb_filepath):
        os.makedirs(rgb_filepath)
    if not os.path.exists(grayscale_filepath):
        os.makedirs(grayscale_filepath)
    count = 0
    axis = [0.0, 0.0, 0.0]
    # start_load_time = time.time()
    my_mesh = mesh.Mesh.from_file(stl_filepath)
    # end_load_time = time.time()
    # print("Image: {}; Load time: {}s".format(stl_filepath, end_load_time-start_load_time))

    for i in range(len(axis)):
        # Iterates over the axis
        axis = [0.0, 0.0, 0.0]
        axis[i] += 0.5
        for k in range(0, 4):
            # for radians in range(0,90,30):
            rgb_filename = filename + "{}.jpeg".format(count)
            radians = random.randint(0, 91)
            # my_mesh_copy = copy.copy(my_mesh)
            # start_mutation_time = time.time()
            my_mesh.rotate(axis, math.radians(radians))
            # Apply translation
            x_translation = random.randint(0, 50)
            y_translation = random.randint(0, 50)

            my_mesh.x += x_translation
            my_mesh.y += y_translation
            # end_mutation_time = time.time()
            # print("Time modifications: {}".format(end_mutation_time-start_mutation_time))

            # start_write_time = time.time()
            write_stl_data_to_img(my_mesh, rgb_filepath + rgb_filename)
            # end_write_time = time.time()
            # print("Saving time: {}".format(end_write_time-start_write_time))
            rgb_to_grayscale(rgb_filepath + rgb_filename, grayscale_filepath + rgb_filename)

            image_contents = tf.io.read_file(grayscale_filepath + rgb_filename)
            image = tf.image.decode_jpeg(image_contents, channels=3)
            image = tf.image.resize(image, [width, height])
            expanded_img = tf.expand_dims(image, axis=0)
            predictions = reconstructed_model.predict(expanded_img)
            predictions_list.append(predictions)
            # Turn to original
            my_mesh.rotate(axis, -math.radians(radians))
            my_mesh.x -= x_translation
            my_mesh.y -= y_translation
            count += 1
    shutil.rmtree(rgb_filepath)
    shutil.rmtree(grayscale_filepath)
    col_totals = [sum(x) for x in zip(*predictions)]
    return col_totals


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training models')
    parser.add_argument("model_filepath",
                        type=str,
                        help="Model filepath")
    parser.add_argument("stl_filepath",
                        type=str,
                        help=".stl filepath")
    parser.add_argument("--width",
                        type=int,
                        help="Width of the images",
                        default=480)
    parser.add_argument("--height",
                        type=int,
                        help="Height of the images",
                        default=640)
    args = parser.parse_args()

    predictions = predict(args.model_filepath, args.stl_filepath, args.width, args.height)
    print(predictions)