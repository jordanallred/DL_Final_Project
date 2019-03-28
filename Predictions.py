from Data_Utils import get_split_dataset, CNN_data_prep, LSTM_data_prep
import LSTM
import RF
import SVM
import KNN
import CNN
from sklearn.model_selection import train_test_split
from numpy import shape
from numpy import reshape
from numpy import array
from sklearn.metrics import accuracy_score

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Augmented Dataset\\"

def prediction_distribution(predictions, true_labels):
    if len(predictions) != len(true_labels):
        print("Decisions are not same length.")
        print("Predictions length is " + str(len(predictions)))
        print("Labels length is " + str(len(true_labels)))
        exit(-1)
    buy_total, sell_total, hold_total = 0, 0, 0
    buy, sell, hold = 0, 0, 0
    for index in range(len(predictions)):
        if true_labels[index] == 1:
            buy_total += 1
            if predictions[index] == 1:
                buy += 1
        if true_labels[index] == 0:
            hold_total += 1
            if predictions[index] == 0:
                hold += 1
        if true_labels[index] == -1:
            sell_total += 1
            if predictions[index] == -1:
                sell += 1
    print("Correct Buy Percentage: " + str(buy / buy_total))
    print("Correct Hold Percentage: " + str(hold / hold_total))
    print("Correct Sell Percentage: " + str(sell / sell_total))

# features, labels = get_split_dataset('amazon')
# X_train, X_test, y_train, y_test = train_test_split(features, labels, train_size=0.80)

# predictions, true_labels = KNN.predict(X_train, y_train, X_test, y_test)
# accuracy = accuracy_score(true_labels, predictions)
# print("KNN Accuracy: " + str(accuracy))
# prediction_distribution(predictions, true_labels)

# predictions, true_labels = SVM.predict(X_train, y_train, X_test, y_test)
# accuracy = accuracy_score(true_labels, predictions)
# print("SVM Accuracy: " + str(accuracy))

# predictions, true_labels = RF.predict(X_train, y_train, X_test, y_test)
# accuracy = accuracy_score(true_labels, predictions)
# print("Random Forest Accuracy: " + str(accuracy))
# prediction_distribution(predictions, true_labels)

features, labels = get_split_dataset('amazon')
for index in range(9):
    new_features = []
    for feature in features:
        new_features.append(feature[:index] + feature[index + 1:])
    X_train, X_test, y_train, y_test = train_test_split(new_features, labels, train_size=0.80)
    X_train, y_train, X_test, y_test = LSTM_data_prep(X_train, y_train, X_test, y_test)
    predictions, true_labels = LSTM.predict(X_train, y_train, X_test, y_test)
    accuracy = accuracy_score(true_labels, predictions)
    print("Eliminating Feature " + str(index))
    print("LSTM Accuracy: " + str(accuracy) + "\n")
    # prediction_distribution(predictions, true_labels)

'''
features, labels = CNN_data_prep('amazon')
X_train, X_test, y_train, y_test = train_test_split(features, labels, train_size=0.80)
y_train = reshape(y_train, (1012, 390))
predictions, true_labels = CNN.predict(X_train, y_train, X_test, y_test)
accuracy = accuracy_score(true_labels, predictions)
print("CNN Accuracy: " + str(accuracy))
prediction_distribution(predictions, true_labels)
'''
