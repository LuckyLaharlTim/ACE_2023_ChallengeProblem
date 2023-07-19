import re
import tensorflow as tf
import tensorflow_datasets as tfds
import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
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
  tf.keras.layers.Dense(3000, activation='sigmoid'),
  tf.keras.layers.Dense(3000, activation='sigmoid'),
  tf.keras.layers.Dense(1024, activation='sigmoid'),
  tf.keras.layers.Dense(512, activation='sigmoid'),
  tf.keras.layers.Dense(128, activation='sigmoid'),
  tf.keras.layers.Dense(10)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

model.fit(x = X_train, y = y_train, epochs=6, validation_data = (X_test, y_test))
