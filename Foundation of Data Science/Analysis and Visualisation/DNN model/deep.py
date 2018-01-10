from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from sklearn.metrics import mean_squared_error,r2_score
import numpy as np
from data import X_train, X_test, Y_train, Y_test

total_len = X_train.shape[0]

#store the config
log_dir='/Users/shenyi/Desktop/group'


# Parameters
learning_rate = 0.001
training_epochs = 4000
show_step=1000
batch_size = 100
display_step = 20
dropout_rate = 0.9
keep=0.8

# Network Parameters
n_hidden_1 = 32 # 1st layer number of features
n_hidden_2 = 200 # 2nd layer number of features
n_hidden_3 = 200
n_hidden_4 = 256
n_input = X_train.shape[1]
n_classes = 1

# tf Graph input

x = tf.placeholder("float", [None, 12])
y = tf.placeholder("float", [None, 1])
keep_prob = tf.placeholder(tf.float32)


# Create model
def model(x, weights, biases,keep_prob):
    with tf.name_scope("dnn"):
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        tf.summary.histogram('layer_1', layer_1)
        layer_1 = tf.nn.relu(layer_1)


        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        tf.summary.histogram('layer_2', layer_2)
        layer_2 = tf.nn.relu(layer_2)
        drop_out_2 = tf.nn.dropout(layer_2, keep_prob)

        layer_3 = tf.add(tf.matmul(drop_out_2, weights['h3']), biases['b3'])
        tf.summary.histogram('layer_3', layer_3)
        layer_3 = tf.nn.relu(layer_3)
        drop_out_3 = tf.nn.dropout(layer_3, keep_prob)

        layer_4 = tf.add(tf.matmul(drop_out_3, weights['h4']), biases['b4'])
        tf.summary.histogram('layer_4', layer_4)
        layer_4 = tf.nn.relu(layer_4)

        out_layer = tf.matmul(layer_4, weights['out']) + biases['out']
        return out_layer

# Store layers weight & bias
with tf.name_scope("weights-biases"):
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1], 0, 0.1)),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], 0, 0.1)),
        'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3], 0, 0.1)),
        'h4': tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4], 0, 0.1)),
        'out': tf.Variable(tf.random_normal([n_hidden_4, n_classes], 0, 0.1))
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1], 0, 0.1)),
        'b2': tf.Variable(tf.random_normal([n_hidden_2], 0, 0.1)),
        'b3': tf.Variable(tf.random_normal([n_hidden_3], 0, 0.1)),
        'b4': tf.Variable(tf.random_normal([n_hidden_4], 0, 0.1)),
        'out': tf.Variable(tf.random_normal([n_classes], 0, 0.1))
    }
saver = tf.train.Saver()
# Construct model
with tf.name_scope("train"):
    y_pred = model(x, weights, biases,keep)
    cost = tf.reduce_mean(tf.square(y_pred-y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
tf.summary.scalar('cost',cost)



# Launch the graph
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(log_dir + '/train', sess.graph)
    test_writer = tf.summary.FileWriter(log_dir + '/test')
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(total_len/batch_size)
        # Loop over all batches
        for i in range(total_batch-1):
            batch_x = X_train[i*batch_size:(i+1)*batch_size]
            batch_y = Y_train[i*batch_size:(i+1)*batch_size]
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c, p = sess.run([optimizer, cost, y_pred], feed_dict={x: batch_x,
                                                          y: batch_y})
            # Compute average loss
            avg_cost += c / total_batch

        # sample prediction
        label_value = batch_y
        estimate = p
        err = label_value-estimate
        #print ("num batch:", total_batch)

        # Display logs per epoch step
        if epoch % display_step == 0:
            print ("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))
            print ("[*]----------------------------")
            summary= sess.run(merged, feed_dict={x: batch_x,y: batch_y})
            train_writer.add_summary(summary, epoch)
            #for i in range(20):
            #    print ("label value:", label_value[i], "estimated value:", estimate[i])
            #print ("[*]============================")

    # Test model
        if epoch % show_step==0:
            accuracy = sess.run(cost, feed_dict={x: X_test, y: Y_test})
            tf.summary.scalar('MSE of test set',accuracy)

    accuracy = sess.run(cost, feed_dict={x: X_test, y: Y_test})
    predicted_vals = sess.run(y_pred, feed_dict={x: X_test})
    saver_path = saver.save(sess, log_dir+"/save/model.ckpt")
    print ("Cost on test set:", "{:.9f}".format(accuracy))
    print('Coefficient:',"{:.9f}".format(r2_score(Y_test,predicted_vals)))
    #plot_delta(Y_test=Y_test, Y_pred=predicted_vals)

#summarise
'''

'''
