from django.shortcuts import render
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
import threading
from threading import Thread, Lock
import time

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
set_session(sess)
K.set_session(sess)
graph = tf.get_default_graph()

self.states, self.actions, self.rewards = [], [], []

self.image_memory = np.zeros(self.state_size)
