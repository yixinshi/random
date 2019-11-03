import tensorflow as tf
from itertools import repeat
#from tensorflow.contrib.nccl import all_sum
#from tensorflow.nccl import all_sum
from tensorflow.python.ops import nccl_ops as nccl
with tf.device('/gpu:0'):
    g0 = tf.placeholder(tf.float32, (2, 2), "g0")
with tf.device('/gpu:1'):
    g1 = tf.placeholder(tf.float32, (2, 2), "g1")
all_reduce_sum = nccl.all_sum([g0, g1])
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True,
                                        allow_soft_placement=False))
init = tf.global_variables_initializer()
sess.run(init)
r = [[1, 1], [1, 1]], [[2, 2], [2, 2]]
for x, y in repeat(r):
    sess.run(all_reduce_sum, feed_dict={g0: x, g1: y})

#https://github.com/tensorflow/tensorflow/issues/30100
import tensorflow as tf
from tensorflow.python.ops import nccl_ops as nccl
with tf.device('/gpu:0'):
    a = tf.constant([1,2,3,4,5], dtype=tf.float32)
with tf.device('/gpu:1'):
    b = tf.constant([6,7,8,9,10], dtype=tf.float32)
with tf.device('/gpu:0'):
    c = tf.identity(nccl.reduce_sum([a, b]))
sess = tf.Session()
print(sess.run(c)) 
