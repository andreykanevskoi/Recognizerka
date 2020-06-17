from flask import Flask, request
from flask.templating import render_template

from tensorflow.keras import layers
from tensorflow import keras
from matplotlib import pyplot as plt

import numpy as np
import tensorflow as tf

import PIL.Image
import PIL.ImageOps
import base64
import os

N = 5
k = 0

RUS_CHARS = [
    'А'.encode('utf-8'),
    'Б'.encode('utf-8'),
    'В'.encode('utf-8'),
    'Г'.encode('utf-8'),
    'Д'.encode('utf-8'),
    'Е'.encode('utf-8'),
    'Ж'.encode('utf-8'),
    'З'.encode('utf-8'),
    'И'.encode('utf-8'),
    'Й'.encode('utf-8'),
    'К'.encode('utf-8'),
    'Л'.encode('utf-8'),
    'М'.encode('utf-8'),
    'Н'.encode('utf-8'),
    'О'.encode('utf-8'),
    'П'.encode('utf-8'),
    'Р'.encode('utf-8'),
    'С'.encode('utf-8'),
    'Т'.encode('utf-8'),
    'У'.encode('utf-8'),
    'Ф'.encode('utf-8'),
    'Х'.encode('utf-8'),
    'Ц'.encode('utf-8'),
    'Ч'.encode('utf-8'),
    'Ш'.encode('utf-8'),
    'Щ'.encode('utf-8'),
    'Ъ'.encode('utf-8'),
    'Ы'.encode('utf-8'),
    'Ь'.encode('utf-8'),
    'Э'.encode('utf-8'),
    'Ю'.encode('utf-8'),
    'Я'.encode('utf-8'),
    'Ё'.encode('utf-8'),
    'а'.encode('utf-8'),
    'б'.encode('utf-8'),
    'в'.encode('utf-8'),
    'г'.encode('utf-8'),
    'д'.encode('utf-8'),
    'е'.encode('utf-8'),
    'ж'.encode('utf-8'),
    'з'.encode('utf-8'),
    'и'.encode('utf-8'),
    'й'.encode('utf-8'),
    'к'.encode('utf-8'),
    'л'.encode('utf-8'),
    'м'.encode('utf-8'),
    'н'.encode('utf-8'),
    'о'.encode('utf-8'),
    'п'.encode('utf-8'),
    'р'.encode('utf-8'),
    'с'.encode('utf-8'),
    'т'.encode('utf-8'),
    'у'.encode('utf-8'),
    'ф'.encode('utf-8'),
    'х'.encode('utf-8'),
    'ц'.encode('utf-8'),
    'ч'.encode('utf-8'),
    'ш'.encode('utf-8'),
    'щ'.encode('utf-8'),
    'ъ'.encode('utf-8'),
    'ы'.encode('utf-8'),
    'ь'.encode('utf-8'),
    'э'.encode('utf-8'),
    'ю'.encode('utf-8'),
    'я'.encode('utf-8'),
    'ё'.encode('utf-8'),
]

def get_char_from_pred(prediction):
    print('+======== P ========+')	
    p = np.array(prediction)
    np.set_printoptions(precision=3)
    print(p)
    p = p.argsort()[::-1]
    clist = []
    for i in range(N):
        clist.append(RUS_CHARS[p[i]].decode('utf-8'))
    print (clist)
    return clist


def create_model():
    model = tf.keras.models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)))
    model.add(layers.Dropout(rate=0.3))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Dropout(rate=0.3))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(66))
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    return model

def predict(img):
    img = img.convert('L').resize((32,32))
    img.save("./test.png","PNG")
    print("ARR", np.array(img))
    arr = np.array([ np.array(img).reshape(32,32)[:, :, np.newaxis] ])

    model = create_model()
    model.load_weights('./tf_model/weights')
    print(arr.shape)
    prediction = model.predict(arr)
    prediction = prediction[0]
    #print(prediction)
    return get_char_from_pred(prediction)


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('hello.html', name='GET')
    if request.method == 'POST':
        user_img = request.form['img']
        imgdata = base64.b64decode(user_img[22:])
        filename = 'temp.png' 
        with open(filename, 'wb') as f:
            f.write(imgdata)
        img = PIL.Image.open('temp.png')
        pr = predict(img)
        print('+======== PREDICTION ========+')	
        print(pr)
        return {'responseText': pr}

if __name__ == '__main__':
    app.run(debug=True)



