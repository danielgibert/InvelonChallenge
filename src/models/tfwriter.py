import tensorflow as tf
import csv


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def image_example(image_string, label):
    """
    Codification of a single image example
    :param image_string: str
    :param label: int
    :return: tf.train.Example
    """
    image_shape = tf.image.decode_jpeg(image_string).shape
    feature = {
      'height': _int64_feature(image_shape[0]),
      'width': _int64_feature(image_shape[1]),
      'depth': _int64_feature(image_shape[2]),
      'label': _int64_feature(label),
      'image_raw': _bytes_feature(image_string),
    }
    return tf.train.Example(features=tf.train.Features(feature=feature))


def write_grayscale_images_to_tfrecords(csv_filepath, tfrecord_file):
    """
    Write the grayscale images defined in the csv file into TFRecords
    :param csv_filepath: str
    :param tfrecords_filepath: str
    :return: None
    """
    with tf.io.TFRecordWriter(tfrecord_file) as tfwriter:
        with open(csv_filepath, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(row["filename"], row['ID'])
                #Load png to numpy
                image_contents = tf.io.read_file(row["filename"])
                image = tf.image.decode_jpeg(image_contents, channels=3)
                img_string = tf.io.encode_jpeg(image)
                label = int(row['ID'])
                example = image_example(img_string, label)
                tfwriter.write(example.SerializeToString())


#write_grayscale_images_to_tfrecords("../../data/examples/training.csv", "../../data/examples/tfrecords/training.tfrecords")
#write_grayscale_images_to_tfrecords("../../data/examples/validation.csv", "../../data/examples/tfrecords/validation.tfrecords")