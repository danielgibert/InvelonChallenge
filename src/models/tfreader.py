import tensorflow as tf

def _parse_tfrecord_function(example, width, height):
    """
    Parses a single TFRecord row
    :param example: instance
    :param width: int
    :param height: int
    :return: decoded_img, category
    """
    image_feature_description = {
        'height': tf.io.FixedLenFeature([], tf.int64),
        'width': tf.io.FixedLenFeature([], tf.int64),
        'depth': tf.io.FixedLenFeature([], tf.int64),
        'label': tf.io.FixedLenFeature([], tf.int64),
        'image_raw': tf.io.FixedLenFeature([], tf.string),
    }
    parsed = tf.io.parse_single_example(example, image_feature_description)

    decoded_img = tf.io.decode_image(parsed['image_raw'])
    decoded_img = tf.reshape(decoded_img, (parsed['width'],
                                           parsed['height'],
                                           parsed['depth']))
    decoded_img = tf.image.resize(decoded_img, [width, height])  # Resize image

    decoded_img = tf.cast(decoded_img, tf.float32) / 255.0  # convert image to floats in [0, 1] range
    return decoded_img, parsed['label']

def make_dataset(filepath, SHUFFLE_BUFFER_SIZE=1024, BATCH_SIZE=1, WIDTH=480, HEIGHT=640):
    """
    Creates a dataset from a TFRecord file
    :param filepath: str
    :param SHUFFLE_BUFFER_SIZE: int
    :param BATCH_SIZE: int
    :param WIDTH: int
    :param HEIGHT: int
    :return: TFRecord.dataset
    """
    dataset = tf.data.TFRecordDataset(filepath)
    dataset = dataset.shuffle(SHUFFLE_BUFFER_SIZE)
    #dataset = dataset.repeat(EPOCHS)
    dataset = dataset.map(lambda x: _parse_tfrecord_function(x, WIDTH, HEIGHT))
    dataset = dataset.batch(batch_size=BATCH_SIZE)
    return dataset