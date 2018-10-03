import tensorflow as tf
import numpy as np
# import getTrajectories
from tensorflow.contrib import rnn
import getStandardIntersectionTrip
from sklearn import preprocessing

time_steps = 12 #
num_units = 128 # hidden layer units
n_input = 3 # (streetNum,aveNum,label)
learning_rate = 0.001
n_classes = 2 #
batch_size = 128

trip_data = getStandardIntersectionTrip.finalTrip3
label_data = getStandardIntersectionTrip.Label_two_classes
trip_input = []
label_input = []

oneHotLabel_three_classes = []
oneHotLabel_two_classes = []

enc_3 = preprocessing.OneHotEncoder()
enc_3.fit([[0],[1],[2]])
enc_2 = preprocessing.OneHotEncoder()
enc_2.fit([[0],[1]])

# ------------------get batch_x & batch_y-------------------
count = 0
jj = 0
for trip in trip_data:
    if(len(trip)>time_steps):
        trip_input.append([])
        ii = 0
        for item in trip[:time_steps]:
            trip_input[jj].append([item[0],item[1],label_data[count][ii]])
            ii+=1
        jj+=1
        label_input.append(label_data[count][:time_steps+1])
    count+=1

trip_input = np.array(trip_input)
label_input = np.array(label_input)
print trip_input.shape
print label_input.shape

iter_num = int(trip_input.shape[0]/batch_size)

processTrip = []
processLabel = []
for ii in range(iter_num):
    processTrip.append([])
    processLabel.append([])
    processTrip[ii] = trip_input[ii*batch_size:(ii+1)*batch_size]
    processLabel[ii] = label_input[ii*batch_size:(ii+1)*batch_size][:,-1]
    processLabel[ii]=processLabel[ii].reshape((batch_size,1))

processTrip = np.array(processTrip)
processLabel = np.array(processLabel)
print(processTrip.shape)
print(processLabel.shape)

for ii in range(len(processLabel)):
    oneHotLabel_two_classes.append([])
    for label in processLabel[ii]:
        oneHotLabel_two_classes[ii].append(enc_2.transform(label[0]).toarray())

oneHotLabel_two_classes = np.array(oneHotLabel_two_classes)
print(oneHotLabel_two_classes.shape)

# ------------------set parameters-------------------

out_weights = tf.Variable(tf.random_normal([num_units,n_classes]))
out_bias = tf.Variable(tf.random_normal([n_classes]))

x = tf.placeholder("float",[None,time_steps,n_input])
y = tf.placeholder("float",[None,n_classes])

# input = tf.matmul(x,in_weights)+in_bias
input = tf.unstack(x,time_steps,1)

lstm_layer = rnn.BasicLSTMCell(num_units,forget_bias=1)
outputs,_=rnn.static_rnn(lstm_layer,input,dtype="float32")
prediction = tf.matmul(outputs[-1],out_weights)+out_bias

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y))
opt = tf.train.AdamOptimizer(learning_rate).minimize(loss)

correct_prediction = tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

print('--------------------rnn---------------------')
print ('time_step', time_steps)
print ('num_units', num_units)
print('learning_rate',learning_rate)
print('n_classes',n_classes)
print('batch_size',batch_size)


init = tf.global_variables_initializer()

'''
# with tf.Session() as sess:
#     sess.run(init)
#     batch_x = getTrajectories.finalTrip
#     batch_y = getTrajectories.oneHotLabel2[:, -1]
#     batch_x = batch_x.reshape((batch_size, time_steps, n_input))
#     # batch_y = batch_y.reshape((batch_size,time_steps,n_classes))
#     sess.run(opt, feed_dict={x: batch_x, y: batch_y})
#     acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
#     los = sess.run(loss, feed_dict={x: batch_x, y: batch_y})
#     print ("Accuracy", acc)
#     print ("Loss", los)
#     print ("y", batch_y)
#     print ("pred", sess.run(prediction, feed_dict={x: batch_x, y: batch_y}))
'''


image_summary = tf.summary.image
scalar_summary = tf.summary.scalar
histogram_summary = tf.summary.histogram
merge_summary = tf.summary.merge
SummaryWriter = tf.summary.FileWriter

with tf.name_scope('loss'):
    loss_summary = scalar_summary('loss', loss)
with tf.name_scope('accuracy'):
    acc_summary = scalar_summary('accuracy', accuracy)

merged = tf.summary.merge_all()

with tf.Session() as sess:
    sess.run(init)
    writer = SummaryWriter('/Users/liangao/Desktop/logs_122', sess.graph)
    iter = 1
    while (iter<(iter_num+1)):
        batch_x = processTrip[iter-1]
        batch_y = oneHotLabel_two_classes[iter-1]
        batch_x = batch_x.reshape((batch_size, time_steps, n_input))
        batch_y = batch_y.reshape((batch_size,n_classes))
        sess.run(opt, feed_dict={x: batch_x, y: batch_y})
        acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
        los = sess.run(loss, feed_dict={x: batch_x, y: batch_y})
        summary, _ = sess.run([merged, opt], feed_dict={x: batch_x, y: batch_y})
        # merged = tf.summary.merge([loss_summary, acc_summary])
        # result = sess.run(merged)
        # summary, _ = sess.run(merged, feed_dict={x: batch_x, y: batch_y})
        # writer.add_summary(result,iter)
        writer.add_summary(summary,iter)
        print ("Accuracy", acc)
        print ("Loss", los)
        # print ("y", batch_y)
        # print ("pred", sess.run(prediction, feed_dict={x: batch_x, y: batch_y}))
        iter += 1





