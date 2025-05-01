import math
import tensorflow as tf
from tensorflow.keras import activations, layers, models
from hyperparameters import NOISE_EMBEDDING_SIZE, IMAGE_SIZE

def sinusoidal_embedding(x):
    frequencies = tf.exp(tf.linspace( tf.math.log(1.0), tf.math.log(1000.0), NOISE_EMBEDDING_SIZE // 2))
    angular_speeds = 2.0 * math.pi * frequencies
    embeddings = tf.concat([tf.sin(angular_speeds * x), tf.cos(angular_speeds * x)], axis=3)
    return embeddings

def ResidualBlock(width):
    def apply(x):
        input_width = x.shape[3]
        if input_width == width:
            residual = x
        else:
            residual = layers.Conv2D(width, kernel_size=1)(x)
        x = layers.BatchNormalization(center=False, scale=False)(x)
        x = layers.Conv2D(width, kernel_size=3, padding="same", activation=activations.swish)(x)
        x = layers.Conv2D(width, kernel_size=3, padding="same")(x)
        x = layers.Add()([x, residual])
        return x

    return apply

def DownBlock(width, block_depth):
    def apply(x):
        x, skips = x
        for _ in range(block_depth):
            x = ResidualBlock(width)(x)
            skips.append(x)
        x = layers.AveragePooling2D(pool_size=2)(x)
        return x

    return apply

def UpBlock(width, block_depth):
    def apply(x):
        x, skips = x
        x = layers.UpSampling2D(size=2, interpolation="bilinear")(x)
        for _ in range(block_depth):
            x = layers.Concatenate()([x, skips.pop()])
            x = ResidualBlock(width)(x)
        return x
    return apply


def get_unet():
    noisy_images = layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    x = layers.Conv2D(32, kernel_size=1)(noisy_images)

    noise_variances = layers.Input(shape=(1, 1, 1))
    noise_embedding = layers.Lambda(lambda x: sinusoidal_embedding(x), output_shape=(1, 1, 32))(noise_variances)
    noise_embedding = layers.UpSampling2D(size=IMAGE_SIZE, interpolation="nearest")(noise_embedding)

    x = layers.Concatenate()([x, noise_embedding])

    skips = []
    x = DownBlock(32, block_depth=2)([x, skips])
    x = DownBlock(64, block_depth=2)([x, skips])
    x = DownBlock(96, block_depth=2)([x, skips])
    x = ResidualBlock(128)(x)
    x = ResidualBlock(128)(x)
    x = UpBlock(96, block_depth=2)([x, skips])
    x = UpBlock(64, block_depth=2)([x, skips])
    x = UpBlock(32, block_depth=2)([x, skips])
    x = layers.Conv2D(3, kernel_size=1, kernel_initializer="zeros")(x)
    return models.Model([noisy_images, noise_variances], x, name="unet")