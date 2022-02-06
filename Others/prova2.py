from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.models import load_model

from numpy import genfromtxt
import numpy as np

my_data = genfromtxt('edo.csv', delimiter=',')

x_train = my_data[:700, 0:4]
y_train = to_categorical(my_data[:700, 4:5], num_classes=3)

x_test = my_data[700:, 0:4]
y_test = to_categorical(my_data[700:, 4:5], num_classes=3)




# Define a simple sequential model
def create_model():
    model = Sequential()
    model.add(Dense(12, input_dim=4, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

model = create_model()


# print('Accuracy: %.2f' % (accuracy*100))
# model.save("model.h5")
# model.summary()
# # Load the model
# my_model = load_model("model.h5")
# # Load the test data file and make predictions on it
# v = np.array([[1.0, 0.0, 0.0, 0.0]])

#
# print(my_model.predict(v), my_model.predict_classes(v))

# # Create a new model instance
# model = create_model()

# Load the previously saved weights
model.load_weights("./checkpoints/weights-improvement-397-0.999.hdf5")

# Re-evaluate the model
loss, acc = model.evaluate(x_test,  y_test, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100*acc))

v = np.array([[0.6, 0.7, 0.8, 0.9]])

print(model.predict(v), model.predict_classes(v))

model.fit(x_train, y_train, epochs=500, batch_size=10, verbose=2)

