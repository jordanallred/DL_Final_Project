from sklearn.ensemble import RandomForestClassifier
from numpy import ndarray


def predict(train_features: ndarray, train_labels: ndarray, test_features: ndarray, test_labels: ndarray):
    classifier = RandomForestClassifier(n_estimators=25)
    classifier.fit(train_features, train_labels.ravel())
    predictions = classifier.predict(test_features)
    rounded_predictions = []
    for prediction in predictions:
        rounded_predictions.append(round(prediction))

    return test_labels, rounded_predictions
