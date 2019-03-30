from Data_Utils import CNN_data_prep, LSTM_data_prep, CNN_test_data_prep
import LSTM
import RF
import SVM
import KNN
import CNN
from numpy import shape
from numpy import reshape
from numpy import array
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from random import randint

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Augmented Dataset\\"

def prediction_distribution(predictions: list, true_labels: list):
    if len(predictions) != len(true_labels):
        print("Decisions are not same length.")
        print("Predictions length is " + str(len(predictions)))
        print("Labels length is " + str(len(true_labels)))
        exit(-1)
    buy_total, sell_total, hold_total = 0, 0, 0
    buy, sell, hold = 0, 0, 0
    buy_fp, sell_fp, hold_fp = 0, 0, 0
    for index in range(len(predictions)):
        if true_labels[index] == 1:
            buy_total += 1
            if predictions[index] == 1:
                buy += 1
            elif predictions[index] == 0:
                hold_fp += 1
            elif predictions[index] == -1:
                sell_fp += 1
        if true_labels[index] == 0:
            hold_total += 1
            if predictions[index] == 0:
                hold += 1
            elif predictions[index] == 1:
                buy_fp += 1
            elif predictions[index] == -1:
                sell_fp += 1
        if true_labels[index] == -1:
            sell_total += 1
            if predictions[index] == -1:
                sell += 1
            elif predictions[index] == 1:
                buy_fp += 1
            elif predictions[index] == 0:
                hold_fp += 1
    if buy_total > 0:
        print("Correct Buy Percentage: " + str(100 * buy / buy_total) + "%")
        print("False Positive Buy Percentage: " + str(100 * buy_fp / buy_total) + "%")
        print("Total True Buy Decisions: " + str(buy_total))
    else:
        print("Correct Buy Percentage: N/A")
        print("False Positive Buy Percentage: N/A")
    if hold_total > 0:
        print("Correct Hold Percentage: " + str(100 * hold / hold_total))
        print("False Positive Hold Percentage: " + str(100 * hold_fp / hold_total) + "%")
        print("Total True Hold Decisions: " + str(hold_total))
    else:
        print("Correct Hold Percentage: N/A")
        print("False Positive Hold Percentage: N/A")
    if sell_total > 0:
        print("Correct Sell Percentage: " + str(100 * sell / sell_total) + "%")
        print("False Positive Sell Percentage: " + str(100 * sell_fp / sell_total) + "%")
        print("Total Sell Buy Decisions: " + str(sell_total))
    else:
        print("Correct Sell Percentage: N/A")
        print("False Positive Sell Percentage: N/A")
    print()


def prediction_aggregation(predictions: list):
    if len(predictions) % 2 == 0:
        print("Warning: split votes are possible. Odd number of inputs is required.")
        exit(-1)
    if len(predictions) % 3 == 0:
        print("Warning: split votes are possible. Change number of inputs.")
        exit(-1)
    if len(predictions) == 0:
        print("List is empty.")
        exit(-1)
    length = len(predictions[0])
    for num_methods in range(len(predictions)):
        if len(predictions[num_methods]) != length:
            print("Predictions are of unequal length.")
            exit(-1)
    required_votes = len(predictions) // 2 + 1
    votes = []
    for index in range(len(predictions[0])):
        buy, sell, hold = 0, 0, 0
        for num_methods in range(len(predictions)):
            if predictions[num_methods][index] == 1:
                buy += 1
            elif predictions[num_methods][index] == 0:
                hold += 1
            elif predictions[num_methods][index] == -1:
                sell += 1
            if buy == required_votes:
                votes.append(1)
                break
            elif hold == required_votes:
                votes.append(0)
                break
            elif sell == required_votes:
                votes.append(-1)
                break
            if buy + hold + sell == len(predictions):
                if buy == hold:
                    if randint(0, 1) == 0:
                        votes.append(1)
                    else:
                        votes.append(0)
                elif buy == sell:
                    if randint(0, 1) == 0:
                        votes.append(1)
                    else:
                        votes.append(-1)
                elif sell == hold:
                    if randint(0, 1) == 0:
                        votes.append(0)
                    else:
                        votes.append(-1)
    return votes


def get_features(company: str, train_size=0.80):
    features, labels = CNN_data_prep(company)
    '''
    prices = []
    times = []
    for feature in features:
        for minute in feature:
            times.append(minute[0])
            prices.append(minute[1])
    '''
    features = reshape(features, (shape(features)[0] * shape(features)[1], 8))
    labels = reshape(labels, (shape(labels)[0] * shape(labels)[1], 1))
    X_train = features[:round(len(features) * train_size)]
    # X_test = features[round(len(features) * train_size):]
    y_train = labels[:round(len(labels) * train_size)]
    # y_test = labels[round(len(labels) * train_size):]

    X_test, y_test = CNN_test_data_prep(company)
    prices = []
    times = []

    for day in X_test:
        for minute in day:
            times.append(minute[0])
            prices.append(minute[1])
    X_test = reshape(X_test, (shape(X_test)[0] * shape(X_test)[1], 8))
    y_test = reshape(y_test, (shape(y_test)[0] * shape(y_test)[1], 1))

    # prices = prices[round(len(prices) * train_size):]
    # times = times[round(len(times) * train_size):]
    scaling = MinMaxScaler(feature_range=(-1, 1)).fit(X_train)
    X_train = scaling.transform(X_train)
    X_test = scaling.transform(X_test)
    return X_train, X_test, y_train, y_test, prices, times


def knn_predict(company: str, verbose=False):
    X_train, X_test, y_train, y_test, prices, times = get_features(company, 0.01)
    true_labels, KNN_predictions = KNN.predict(X_train, y_train, X_test, y_test)
    accuracy = accuracy_score(true_labels, KNN_predictions)
    if verbose:
        print("KNN Accuracy: " + str(accuracy * 100) + "%")
        prediction_distribution(KNN_predictions, true_labels)
    return prices, times, KNN_predictions


def svm_predict(company: str, verbose=False):
    X_train, X_test, y_train, y_test, prices, times = get_features(company, 0.01)
    true_labels, SVM_predictions = SVM.predict(X_train, y_train, X_test, y_test)
    accuracy = accuracy_score(true_labels, SVM_predictions)
    if verbose:
        print("SVM Accuracy: " + str(accuracy * 100) + "%")
        prediction_distribution(SVM_predictions, true_labels)
    return prices, times, SVM_predictions


def rf_predict(company: str, verbose=False):
    X_train, X_test, y_train, y_test, prices, times = get_features(company, 1.00)
    true_labels, RF_predictions = RF.predict(X_train, y_train, X_test, y_test)
    accuracy = accuracy_score(true_labels, RF_predictions)
    if verbose:
        print("Random Forest Accuracy: " + str(accuracy * 100) + "%")
        prediction_distribution(RF_predictions, true_labels)
    return prices, times, RF_predictions


def lstm_predict(company:str, verbose=False):
    X_train, X_test, y_train, y_test, prices, times = get_features(company)
    X_train, y_train, X_test, y_test = LSTM_data_prep(X_train, y_train, X_test, y_test)
    LSTM_predictions, true_labels = LSTM.predict(X_train, y_train, X_test, y_test)
    accuracy = accuracy_score(true_labels, LSTM_predictions)
    if verbose:
        print("LSTM Accuracy: " + str(accuracy * 100) + "%")
        prediction_distribution(LSTM_predictions, true_labels)
    return prices, times, LSTM_predictions


def cnn_predict(company: str, verbose=False):
    X_train, X_test, y_train, y_test, prices, times = get_features(company)
    y_train, y_test = reshape(array(y_train), (shape(y_train)[0], 1, 1)), reshape(array(y_test), (shape(y_test)[0], 1, 1))
    true_labels, CNN_predictions = CNN.predict(X_train, y_train, X_test, y_test)
    true_labels = reshape(true_labels, (shape(true_labels)[0], ))
    CNN_predictions = reshape(CNN_predictions, (shape(CNN_predictions)[0], ))
    accuracy = accuracy_score(true_labels, CNN_predictions)
    if verbose:
        print("Training Instances: " + str(len(X_train)))
        print("Testing Instances: " + str(len(X_test)))
        print()
        print("CNN Accuracy: " + str(accuracy * 100) + "%")
        prediction_distribution(CNN_predictions, true_labels)
    return prices, times, CNN_predictions
