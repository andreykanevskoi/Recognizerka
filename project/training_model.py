from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow.keras import layers
from tensorflow import keras

import numpy as np
import tensorflow as tf
import PIL

def getFlatArrayFromImage(path):
  img = PIL.Image.open(path).convert('L')
  arr = np.array(img)

  flat_arr = arr.ravel()
  return flat_arr

path = '/home/andrew/Recognizerka/fonts/png32_rotated.npz'
with np.load(path) as data:
    train_examples = data['x_train']
    train_labels = data['y_train']
    test_examples = data['x_test']
    test_labels = data['y_test']


# inputs = keras.Input(shape=(1024,), name='chars')
# x = layers.Dense(256, activation='relu', name='dense_1')(inputs)
# x = layers.Dense(256, activation='relu', name='dense_2')(x)
# # x = layers.Dense(512, activation='relu', name='dense_3')(x)
# # x = layers.Dense(512, activation='relu', name='dense_4')(x)
# outputs = layers.Dense(66, name='predictions')(x)

# model = keras.Model(inputs=inputs, outputs=outputs)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(8, (2, 2), activation='relu', input_shape=(32, 32, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(66, activation='softmax')
])

x_train = train_examples

new_y_labels = np.zeros(8910)
for i in range(8910):
    new_y_labels[i], = np.where(train_labels[i] == 1)

y_train = new_y_labels

x_test = test_examples

new_y_labels = np.zeros(1782)
for i in range(1782):
    new_y_labels[i], = np.where(test_labels[i] == 1)

y_test = new_y_labels


# *----------------------------*



# *----------------------------*


# Preprocess the data (these are Numpy arrays)
x_train = x_train.reshape(8910, 32, 32, 1).astype('float32') / 255
x_test = x_test.reshape(1782, 32, 32, 1).astype('float32') / 255

y_train = y_train.astype('float32')
y_test = y_test.astype('float32')

# Reserve 10,000 samples for validation
x_val = x_train[-1782:]
y_val = y_train[-1782:]
x_train = x_train[:-1782]
y_train = y_train[:-1782]

model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=1e-3),  # Optimizer
              # Loss function to minimize
              loss=keras.losses.SparseCategoricalCrossentropy(
                  from_logits=True),
              # List of metrics to monitor
              metrics=['sparse_categorical_accuracy'])

print('# Fit model on training data')
history = model.fit(x_train, y_train,
                    batch_size=64,
                    epochs=100,
                    # We pass some validation for
                    # monitoring validation loss and metrics
                    # at the end of each epoch
                    validation_data=(x_val, y_val))

print('\nhistory dict:', history.history)

# Evaluate the model on the test data using `evaluate`
print('\n# Evaluate on test data')
results = model.evaluate(x_test, y_test, batch_size=64)
print('test loss, test acc:', results)

# create seporate test set
files = [
    '18847_l_6.png',
    '19046_u_9.png',
    '19051_l_0.png',
    '19081_l_0.png',
    '19081_u_17.png'
]
path_to_files = "/home/andrew/Recognizerka/fonts/png_32_32/"

flen = len(files)
my_test_x = np.zeros( (flen, 32, 32, 1) )
print(my_test_x.shape)
k = 0
for file in files:
    my_test_x[k] = getFlatArrayFromImage(path_to_files+file).reshape(32, 32, 1)
    k+=1

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print('\n# Generate predictions for 3 samples')
predictions = model.predict(my_test_x)
print('predictions shape:', predictions.shape)


def get_char_from_pred(prediction):
    from draft import RUS_CHARS
    return RUS_CHARS[np.argmax(prediction)].decode('utf-8')

for pred in predictions:
    print(get_char_from_pred(pred))