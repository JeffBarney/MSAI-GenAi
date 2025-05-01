import os
import math
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image
from hyperparameters import IMAGE_SIZE, BATCH_SIZE

def sample_data():
    root_dir = '../image-project-data'
    test_dir = root_dir + '/test'

    # Fetch the styles from our csv of labels
    raw_labels = pd.read_csv(root_dir + '/test_labels.csv')
    styles = raw_labels['style'].dropna().unique()
    styles_sorted = sorted(styles)

    # Build a list of dicts with a style and image sample
    rows = []
    for style in styles:
        img_dir_path = os.path.join(test_dir, style)
        img_file_name = next((img.name for img in os.scandir(img_dir_path) if img.is_file()), None)

        img_tag = f'<img src="{os.path.join(img_dir_path, img_file_name)}" width="{IMAGE_SIZE}">'
        rows.append({
            'Label': style,
            'Image': img_tag
        })

    return pd.DataFrame(rows)


def fetch_data(train=True, num_per_label=math.inf):
    data_dir = '../image-project-data/' + ('train' if train else 'test')
    data = []

    for label in os.listdir(data_dir):
        label_path = os.path.join(data_dir, label)
        num_images = 0
        for image in os.listdir(label_path):
            if num_images > num_per_label:
                break
            
            data.append(os.path.join(label_path, image))
            num_images+=1

    return data

def load_and_normalize(image_path):
    tf_image = tf.io.read_file(image_path)
    tf_image = tf.image.decode_jpeg(tf_image, channels=3)
    tf_image = tf.image.resize(tf_image, (IMAGE_SIZE, IMAGE_SIZE), method='bilinear')
    tf_image = tf.image.convert_image_dtype(tf_image, tf.float32) / 255.0
    return tf_image

def preprocess(images):
    dataset = tf.data.Dataset.from_tensor_slices(images)
    dataset = dataset.map(load_and_normalize, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.shuffle(1000, seed=42)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset
