#
#  Скрипт server.py
#  Предназначен для запуска сервера и обработки запросов
#  Запускает сервер, определяет функции для вызова по маршрутам
#
#  Разработчик: Каневской Андрей
#  Таганрог 2020г
#

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

import project_const as P

# количество наилучших вариантов, выводимых пользователю
N = 5

# k = 0

# выводит список наиболее подходящих букв
# на вход принимает массив с предсказанием нейронной сети
def get_char_from_pred(prediction):	
    p = np.array(prediction) # получили массив
    p = p.argsort()[::-1] # отсортировали по возрастанию (в массиве индексы) и развернули его
    clist = []
    for i in range(N):
        clist.append(P.RUS_CHARS[p[i]].decode('utf-8'))
    return clist

# функция для построения конфигурации модели нейронной сети
def create_model():
    # создание модели нейронной сети
    model = tf.keras.models.Sequential()
    # слой свёртки с 2D ядром
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)))
    # обнуление 30% нейронов для предотвращения переобучения
    model.add(layers.Dropout(rate=0.3))
    # срез половины нейронов
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Dropout(rate=0.3))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    # переход к обычным нейросетям
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(66))
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    return model

# функция, принимающая на вход изображение и вызывающая нейронную сеть
def predict(img):
    img = img.convert('L').resize((32,32)) # получаем картинку, обрабатываем её
    img.save("./test.png","PNG")
    arr = np.array([ np.array(img).reshape(32,32)[:, :, np.newaxis] ]) # делаем трехмерной (32х32х1)
    model = create_model() # создаем модель
    model.load_weights('./tf_model/weights') # загружаем готовые веса
    prediction = model.predict(arr) # совершаем предсказание
    prediction = prediction[0]
    return get_char_from_pred(prediction)

# создаем веб-приложение на основе Flask
app = Flask(__name__)

# прописываем маршрут для GET и POST запроса
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', name='GET')
    if request.method == 'POST':
        user_img = request.form['img'] # получаем base64 код изображения
        imgdata = base64.b64decode(user_img[22:]) # удаляем meta-информацию
        filename = 'temp.png' # сохраняем файл в бинарном представлении
        with open(filename, 'wb') as f:
            f.write(imgdata)
        img = PIL.Image.open('temp.png') # открываем файл как матрицу
        pr = predict(img) # получаем массив вероятных букв (обработанное предсказание нейронной сети)
        return {'responseText': pr} # отправляем его пользователю

if __name__ == '__main__':
    app.run(debug=True)



