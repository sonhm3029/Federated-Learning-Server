from tensorflow import keras
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

from ivirse.common import NDArrays


import numpy as np
from typing import Optional, Tuple

IMG_SIZE = (160, 160)
IMG_SHAPE = (160, 160, 3)
MEAN = [0.23740229, 0.23729787, 0.23700129]
STD = [0.23173477, 0.23151317, 0.23122775]
classes = ["NO", "YES"]
DATASET = "datasets/braintumor"


# Model

preprocess_input = keras.applications.mobilenet_v2.preprocess_input
base_model = keras.applications.MobileNetV2(
    input_shape=IMG_SHAPE,
    include_top=False
)

base_model.trainable = False
global_average_layer = keras.layers.GlobalAveragePooling2D()
prediction_layer = keras.layers.Dense(1)

inputs = keras.Input(shape=IMG_SHAPE)
x = preprocess_input(inputs)
x = keras.layers.Normalization(mean=MEAN, variance=STD)(x)
x = base_model(x, training=False)
x = global_average_layer(x)
x = keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = keras.Model(inputs, outputs)


class Model(tf.Module):
    def __init__(self):
      self.model = model
      self.model.compile(optimizer=tf.keras.optimizers.Adam(), loss=keras.losses.BinaryCrossentropy(from_logits=True))

    @tf.function(input_signature=[
        tf.TensorSpec([None, 160, 160, 3], tf.float32),
        tf.TensorSpec([None, ], tf.float32),
    ])
    def train(self, x, y):
      with tf.GradientTape() as tape:
          pred = self.model(x)
          loss = self.model.loss(y, pred)
      gradients = tape.gradient(loss, self.model.trainable_variables)
      self.model.optimizer.apply_gradients(
          zip(gradients, self.model.trainable_variables))
      result = {"loss": loss}
      return result

    @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.string)])
    def save(self, checkpoint_path):
      tensor_names = [weight.name for weight in self.model.weights]
      tensors_to_save = [weight.read_value() for weight in self.model.weights]
      tf.raw_ops.Save(
          filename=checkpoint_path, tensor_names=tensor_names,
          data=tensors_to_save, name='save')
      return {
          "checkpoint_path": checkpoint_path
      }

    @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.string)])
    def restore(self, checkpoint_path):
      restored_tensors = {}
      for var in self.model.weights:
          restored = tf.raw_ops.Restore(
              file_pattern=checkpoint_path, tensor_name=var.name, dt=var.dtype,
              name='restore')
          var.assign(restored)
          restored_tensors[var.name] = restored
      return restored_tensors

    @tf.function(input_signature=[
      tf.TensorSpec(shape=[], dtype=tf.string)
    ])
    def get_trainable_weights(self,str="OK"):
      trainable_weights = [weight.read_value() for weight in self.model.trainable_weights]
      return {
          "weights": trainable_weights[0],
          "bias": trainable_weights[1]
      }

    @tf.function(input_signature=[
        tf.TensorSpec(shape=[1280, 1], dtype=tf.float32),
        tf.TensorSpec(shape=[1,], dtype=tf.float32)
    ])
    def update_weights(self, w, b):
      current_weight = self.model.trainable_variables;
      new_weights = [w, b]
      for current_val, new_val in zip(current_weight, new_weights):
          current_val.assign(tf.convert_to_tensor(new_val, dtype=current_val.dtype))
      return {
          "message": tf.convert_to_tensor([0])
      }



    @tf.function(input_signature=[
        tf.TensorSpec([None, 160, 160, 3], tf.float32)
    ])
    def infer(self, x):
      logits = self.model(x)
      probabilities = tf.nn.sigmoid(x)
      return {
          "output": probabilities,
          "logits": logits
      }

    @tf.function(input_signature=[
      tf.TensorSpec(shape=[], dtype=tf.string)
    ])
    def status(self, str):
      return {
          "message": tf.convert_to_tensor([1])
      }

    @tf.function(input_signature=[
      tf.TensorSpec(shape=[], dtype=tf.string)
    ])
    def summary(self, str="OK"):
      return self.model.summary()
  

def load_data():
    print("Loading data ...")
    test_gen = ImageDataGenerator(rescale=1./255)
    test_batches = test_gen.flow_from_directory(
        DATASET + "/TEST",
        target_size=(160, 160),
        class_mode='binary',
        batch_size=4,
        shuffle=False,
        color_mode="rgb",
        classes=classes
    )
    
    return test_batches

def evaluate(
    server_round: int, parameters: NDArrays
)-> Optional[Tuple[float, float]]:
    """Evaluate function for server side evaluate

    Args:
        server_round (int): Current server round
        parameters (NDArrays): Aggregated parameters to evaluate
    """
    test_batches = load_data()  
    model = Model()

    model.update_weights(parameters[0].reshape(1280, 1), parameters[1])
    criterion = keras.losses.BinaryCrossentropy(from_logits=True)
    test_loss = keras.metrics.Mean(name='test_loss')
    test_accuracy = keras.metrics.BinaryAccuracy(name='test_accuracy')
    total_step = len(test_batches)
    
    for step, (images, labels) in enumerate(test_batches):
        if (step + 1) == total_step:
            break
        predictions = model.infer(images)
        predictions = tf.reshape(predictions["logits"], (4,))
        loss = criterion(labels, predictions)
        
        test_loss(loss)
        test_accuracy(labels, predictions)
        
    return test_loss.result().numpy(), test_accuracy.result().numpy()
        
