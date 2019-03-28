from numpy import ndarray
from sklearn.svm import SVC
from keras.layers import Conv1D, AveragePooling1D, Flatten, Dense
from keras.models import Sequential

def predict(train_features: ndarray, train_labels: ndarray, test_features: ndarray, test_labels: ndarray):
    epochs = 5
    batch_size = 512

    model = Sequential()

    model.add(Conv1D(filters=128, kernel_size=2))

    model.add(AveragePooling1D(strides=1))

    model.add(Conv1D(filters=128, kernel_size=2))

    model.add(AveragePooling1D(strides=1))

    model.add(Flatten())

    model.add(Dense(1, batch_size=batch_size, input_shape=(390,)))

    # Compiling the RNN
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    # Fitting the RNN to the Training set
    model.fit(train_features, train_labels, epochs=epochs, batch_size=batch_size)

    predictions = model.predict(test_features, batch_size=batch_size)

    rounded_predictions = []
    for prediction in predictions:
        rounded_predictions.append(round(prediction[0]))

    print(rounded_predictions)
    return test_labels, rounded_predictions
