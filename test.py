from ivirse.models.brain_tumor import evaluate
import numpy as np

import tensorflow as tf

# Define shapes
weight_shape = (1280, 1)
bias_shape = (1,)

# Initialize weights and biases using desired initialization method
initializer = tf.initializers.GlorotUniform()

weights = initializer(shape=weight_shape)
biases = initializer(shape=bias_shape)

parameters = [weights.numpy(), biases.numpy()]

evaluate(0, parameters=parameters)