import tensorflow as tf
import sys
sys.path.append("../../")
from src.models.tfreader import make_dataset
from tensorflow import keras
import argparse
import json

def create_Xception_model(hyperparameters, IMG_SHAPE=(480,640,3)):
    """
    Creates a pretrained Xception model.
    :param hyperparameters: dict
    :param IMG_SHAPE: tuple
    :return: keras.model
    """
    model = tf.keras.Sequential()
    base_model = tf.keras.applications.Xception(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet',
                                                   pooling="avg")
    #base_model.trainable = False # Freeze
    model.add(base_model)
    model.add(tf.keras.layers.Dropout(0.5))
    # model.add(tf.keras.layers.Dense(hyperparameters["hidden_neurons"], activation="relu"))
    # model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(hyperparameters["categories"], activation="softmax"))
    return model

def create_MobileNetV2_model(hyperparameters, IMG_SHAPE=(480,640,3)):
    """
    Creates a pretrained MobileNetV2 model.
    :param hyperparameters: dict
    :param IMG_SHAPE: tuple
    :return: keras.model
    """
    model = tf.keras.Sequential()
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet',
                                                   pooling='avg')
    #base_model.trainable = False # Freeze
    model.add(base_model)
    model.add(tf.keras.layers.Dropout(0.5))
    # model.add(tf.keras.layers.Dense(hyperparameters["hidden_neurons"], activation="relu"))
    # model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(hyperparameters["categories"], activation="softmax"))
    return model

def create_DenseNet121_model(hyperparameters, IMG_SHAPE=(480,640,3)):
    """
    Creates a pretrained DenseNet model
    :param hyperparameters: dict
    :param IMG_SHAPE: tuple
    :return: keras.model
    """
    model = tf.keras.Sequential()
    base_model = tf.keras.applications.DenseNet121(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet',
                                                   pooling="avg")
    #base_model.trainable = False # Freeze
    model.add(base_model)
    model.add(tf.keras.layers.Dropout(0.5))
    #model.add(tf.keras.layers.Dense(hyperparameters["hidden_neurons"], activation="relu"))
    #model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(hyperparameters["categories"], activation="softmax"))
    return model


def load_hyperparameters(hyperparameters_filepath):
    """
    Loads the hyperparameters of the network into a dictionary-like structure
    :param hyperparameters_filepath: str
    :return: dict
    """
    with open(hyperparameters_filepath, "r") as hyperparameters_file:
        hyperparameters = json.load(hyperparameters_file)
    return hyperparameters

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training models')
    parser.add_argument("model_type",
                        type=str,
                        help="Model type, e.g. Xception")
    parser.add_argument("training_filepath",
                        type=str,
                        help="Training tfrecords filepath")
    parser.add_argument("validation_filepath",
                        type=str,
                        help="Validation tfrecords filepath")
    parser.add_argument("hyperparameters_filepath",
                        type=str,
                        help="Hyperparameters filepath")
    parser.add_argument("--batch_size",
                        type=int,
                        help="Batch size",
                        default=64)
    parser.add_argument("--epochs",
                        type=int,
                        help="Number of epochs",
                        default=50)
    parser.add_argument("--width",
                        type=int,
                        help="Width of the images",
                        default=480)
    parser.add_argument("--height",
                        type=int,
                        help="Height of the images",
                        default=640)
    parser.add_argument("--output_model",
                        type=str,
                        help="Output model",
                        default=None)
    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

    args = parser.parse_args()
    IMG_SHAPE=(args.width, args.height,3)

    hyperparameters = load_hyperparameters(args.hyperparameters_filepath)
    if args.model_type=="xception":
        base_model = create_Xception_model(hyperparameters, IMG_SHAPE)
    if args.model_type=="densenet":
        base_model = create_DenseNet121_model(hyperparameters, IMG_SHAPE)
    if args.model_type=="mobilenetv2":
        base_model = create_MobileNetV2_model(hyperparameters, IMG_SHAPE)
    else:
        base_model = create_Xception_model(hyperparameters, IMG_SHAPE)


    base_model.compile(
    optimizer = keras.optimizers.Adam(0.0001),  # Optimizer
    # Loss function to minimize
    loss = keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics = [keras.metrics.CategoricalAccuracy()],
    )

    train_dataset = make_dataset(args.training_filepath, BATCH_SIZE=args.batch_size, WIDTH=IMG_SHAPE[0],
                                 HEIGHT=IMG_SHAPE[1])
    validation_dataset = make_dataset(args.validation_filepath, BATCH_SIZE=args.batch_size, WIDTH=IMG_SHAPE[0],
                                      HEIGHT=IMG_SHAPE[1])


    early_stopping_cb = tf.keras.callbacks.EarlyStopping(
        patience=10, restore_best_weights=True
    )

    print("Fit model on training data")
    history = base_model.fit(
        train_dataset,
        epochs=args.epochs,
        callbacks=[early_stopping_cb],
        # We pass some validation for
        # monitoring validation loss and metrics
        # at the end of each epoch
        validation_data=validation_dataset,
    )
    print(history)
    if args.output_model is None:
        base_model.save('tmp/model_{}'.format(args.model_type))
    else:
        base_model.save(args.output_model)