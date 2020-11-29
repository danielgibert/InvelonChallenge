import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras


def predict(model_filepath, img_filepath, width=480, height=640):
    """

    :param model_filepath:
    :param img_filepath:
    :param width:
    :param height:
    :return:
    """
    reconstructed_model = keras.models.load_model(model_filepath)
    image_contents = tf.io.read_file(img_filepath)
    image = tf.image.decode_jpeg(image_contents, channels=3)
    image = tf.image.resize(image, [width, height])
    expanded_img = tf.expand_dims(image, axis=0)
    predictions = reconstructed_model.predict(expanded_img)
    return predictions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training models')
    parser.add_argument("model_filepath",
                        type=str,
                        help="Model filepath")
    parser.add_argument("image_filepath",
                        type=str,
                        help="Image filepath")
    parser.add_argument("--width",
                        type=int,
                        help="Width of the images",
                        default=480)
    parser.add_argument("--height",
                        type=int,
                        help="Height of the images",
                        default=640)
    args = parser.parse_args()

    predictions = predict(args.model_filepath, args.image_filepath, args.width, args.height)