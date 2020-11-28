import tensorflow as tf
import sys
sys.path.append("../../")
from src.models.tfreader import make_dataset
from tensorflow import keras


def create_Xception_model(IMG_SHAPE=(480,640,3)):
    feature_layer_shape = (7,7,2048)
    model = tf.keras.Sequential()
    base_model = tf.keras.applications.Xception(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')
    model.add(base_model)
    model.add(tf.keras.layers.Reshape((feature_layer_shape[0] * feature_layer_shape[1] * feature_layer_shape[2],)))
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(2, activation="softmax"))
    return model

def create_MobileNetV2_model(IMG_SHAPE=(480,640,3)):
    feature_layer_shape = (7,7,2048)
    model = tf.keras.Sequential()
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')
    model.add(base_model)
    model.add(tf.keras.layers.Reshape((feature_layer_shape[0] * feature_layer_shape[1] * feature_layer_shape[2],)))
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(2, activation="softmax"))
    return model

def create_DenseNet121_model(IMG_SHAPE=(480,640,3)):
    feature_layer_shape = (7,7,2048)
    model = tf.keras.Sequential()
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')
    model.add(base_model)
    model.add(tf.keras.layers.Reshape((feature_layer_shape[0] * feature_layer_shape[1] * feature_layer_shape[2],)))
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(2, activation="softmax"))
    return model


#IMG_SHAPE = (480,640,3)
IMG_SHAPE = (224,224,3)
xception_model = create_Xception_model(IMG_SHAPE)
xception_model.compile(
    optimizer=keras.optimizers.Adam(),  # Optimizer
    # Loss function to minimize
    loss=keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

train_dataset = make_dataset("../../data/examples/tfrecords/training.tfrecords")
validation_dataset = make_dataset("../../data/examples/tfrecords/validation.tfrecords")


early_stopping_cb = tf.keras.callbacks.EarlyStopping(
    patience=5, restore_best_weights=True
)

print("Fit model on training data")
history = xception_model.fit(
    train_dataset,
    epochs=32,
    callbacks=[early_stopping_cb],
    # We pass some validation for
    # monitoring validation loss and metrics
    # at the end of each epoch
    validation_data=validation_dataset,
)
