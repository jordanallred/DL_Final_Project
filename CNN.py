from numpy import ndarray, shape, reshape
from sklearn.svm import SVC
from keras.layers import Conv1D, AveragePooling1D, Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

def predict(train_features: ndarray, train_labels: ndarray, test_features: ndarray, test_labels: ndarray):
    epochs = 2
    input_shape = (shape(train_features)[1], 1)

    model = Sequential()
    model.add(Conv1D(filters=128, kernel_size=2, input_shape=input_shape))
    model.add(AveragePooling1D(strides=2))
    model.add(Conv1D(filters=128, kernel_size=2))
    model.add(AveragePooling1D(strides=2))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    model.fit(train_features, train_labels, epochs=epochs, verbose=0)

    predictions = model.predict(test_features)

    rounded_predictions = []
    for prediction in predictions:
        predicted = prediction[0][0]
        if -2 <= predicted <= -0.5:
            rounded_predictions.append(-1)
        elif -0.5 < predicted < 0.5:
            rounded_predictions.append(0)
        elif 0.5 <= predicted <= 2:
            rounded_predictions.append(1)
        elif predicted < -1 or predicted > 1:
            print("Value out of range: " + str(predicted))
            exit(-1)
    return test_labels, rounded_predictions
