from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from numpy import ndarray, shape
from keras.callbacks import TensorBoard
import os; os.environ["OMP_NUM_THREADS"] = "4"

def predict(train_features: ndarray, train_labels: ndarray, test_features: ndarray, test_labels: ndarray):
    batch_size = 256
    epochs = 4
    units = 50
    dropout = 0.10

    model = Sequential()
    # tbCallBack = TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

    model.add(LSTM(units=units, return_sequences=True, input_shape=(train_features.shape[1], train_features.shape[2])))
    # model.add(Dropout(dropout))

    model.add(LSTM(units=units, return_sequences=True, recurrent_dropout=True))
    # model.add(Dropout(dropout))

    model.add(LSTM(units=units))
    # model.add(Dropout(dropout))

    model.add(Dense(1, batch_size=batch_size))

    # Compiling the RNN
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    # Fitting the RNN to the Training set
    model.fit(train_features, train_labels, epochs=epochs, batch_size=batch_size, verbose=1)

    predictions = model.predict(test_features, batch_size=batch_size)

    rounded_predictions = []
    for prediction in predictions:
        rounded_predictions.append(round(prediction[0]))

    return test_labels, rounded_predictions
