#
# # first neural network with keras tutorial
# # from numpy import loadtxt
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.utils import to_categorical
# from keras.callbacks import ModelCheckpoint, TensorBoard
# # from tqdm.keras import TqdmCallback
#
#
# def to_string(l):
#     s = ""
#     for i in l:
#         s += str(i) + ","
#     s = s[:-1]
#     return s
#
# def produce_list():
#     tmp = [random.uniform(0, 1.0) for _ in range(4)]
#     if sum(tmp) >= 2.2:
#         tmp.append(2)
#     elif sum(tmp) >= 1.5:
#         tmp.append(1)
#     else:
#         tmp.append(0)
#     return tmp
#
#
# import random
#
# rows = []
#
# with open("edo.csv", "w+") as file:
#
#     for i in range(1000):
#         file.write(to_string(produce_list()))
#         file.write("\n")
#
#
# from numpy import genfromtxt
# import numpy as np
#
#
# my_data = genfromtxt('edo.csv', delimiter=',')
# print(my_data.shape)
#
# x_train = my_data[:700, 0:4]
# y_train = to_categorical(my_data[:700, 4:5], num_classes=3)
#
# x_test = my_data[700:, 0:4]
# y_test = to_categorical(my_data[700:, 4:5], num_classes=3)
#
#
#
# model = Sequential()
# model.add(Dense(12, input_dim=4, activation='relu'))
# model.add(Dense(8, activation='relu'))
# model.add(Dense(output_dim=3, activation='softmax'))
#
#
#
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#
# # checkpoint
# filepath="./checkpoints/weights-improvement-{epoch:02d}-{accuracy:.3f}.hdf5"
# checkpoint = ModelCheckpoint(filepath, monitor='accuracy', verbose=0, period=10, save_best_only=True)
# tbCallBack = TensorBoard(log_dir="./", histogram_freq=0, write_graph=True, write_images=False)
# callbacks_list = [checkpoint, tbCallBack]
#
# model.fit(x_train, y_train, epochs=500, batch_size=10, callbacks=callbacks_list, verbose=2)
#
# model.save("model_file.h5")
#
# _, accuracy = model.evaluate(x_test, y_test)
#
#
#
#
# print('Accuracy: %.2f' % (accuracy*100))
#
# v = np.array([[0.6, 0.7, 0.8, 0.9]])
#
# print(model.predict(v), model.predict_classes(v))
#
#
# # dataset = loadtxt('pima-indians-diabetes.data.csv', delimiter=',')
# # # split into input (X) and output (y) variables
# # X = dataset[:,0:8]
# # y = dataset[:,8]
# #
# # # define the keras model
# # model = Sequential()
# # model.add(Dense(12, input_dim=8, activation='relu'))
# # model.add(Dense(8, activation='relu'))
# # model.add(Dense(1, activation='sigmoid'))
# #
# #
# #
# # # compile the keras model
# # model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# #
# # # fit the keras model on the dataset
# # model.fit(X, y, epochs=1000, batch_size=10, verbose=0)
# #
# # # evaluate the keras model
# # _, accuracy = model.evaluate(X, y)
# # print('Accuracy: %.2f' % (accuracy*100))

a = [1,2,3]
b = [4,5,6]

for x,y in a,b:
    print(x, y)