import tensorflow as tf
import numpy
import os
#disable warning regarding Tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf.__version__
norm = tf.random.normal(shape=(1000,1),mean=0,stddev=1.)
print(norm)
