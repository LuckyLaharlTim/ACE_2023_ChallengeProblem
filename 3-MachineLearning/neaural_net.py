import re
import tensorflow as tf
import tensorflow_datasets as tfds
import csv
from functools import partial
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
import random

feature_df = pd.read_csv('features.csv')

result_df = pd.read_csv('result.csv')

feature_list = []
for index, rows in feature_df.iterrows():
    # Create list for the current row
    feature_list.append(list(rows)[1:])

result_list = []
for index, rows in result_df.iterrows():
    result_list.append(list(rows)[1:])


print(len(feature_list), len(result_list))
combined = list(map(lambda i: [feature_list[i], result_list[i]], range(900)))
random.shuffle(combined)

x = list(map(lambda i: i[0], combined))
y = list(map(lambda i: i[1], combined))
print(len(x[0]))
print(y[0])

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(1297, 1)),
  tf.keras.layers.Dense(2800, activation=partial(tf.nn.leaky_relu, alpha=.01)),
  tf.keras.layers.Dense(4096, activation=partial(tf.nn.leaky_relu, alpha=.01)),
  tf.keras.layers.Dense(2048, activation=partial(tf.nn.leaky_relu, alpha=.01)),
  tf.keras.layers.Dropout(.125),
  tf.keras.layers.Dense(1024, activation=partial(tf.nn.leaky_relu, alpha=.01)),
  tf.keras.layers.Dense(512, activation=partial(tf.nn.leaky_relu, alpha=.01)),
  tf.keras.layers.Dense(128, activation=partial(tf.nn.leaky_relu, alpha=.01)),
  tf.keras.layers.Dense(2, activation='sigmoid')
])


model.compile(
    optimizer=tf.keras.optimizers.Adam(0.0008),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
)


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

model.fit(x = X_train, y = y_train, epochs=11, validation_data = (X_test, y_test))
