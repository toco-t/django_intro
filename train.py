import pandas as pd
import pickle
import sklearn.metrics as metrics
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

candidates = {
    "gmat": [780, 750, 690, 710, 680, 730, 690, 720, 740, 690, 610, 690,
             710, 680, 770, 610, 580, 650, 540, 590, 620, 600, 550, 550,
             570, 670, 660, 580, 650, 660, 640, 620, 660, 660, 680, 650,
             670, 580, 590, 690],
    "gpa": [4, 3.9, 3.3, 3.7, 3.9, 3.7, 2.3, 3.3, 3.3, 1.7, 2.7, 3.7, 3.7,
            3.3, 3.3, 3, 2.7, 3.7, 2.7, 2.3, 3.3, 2, 2.3, 2.7, 3, 3.3, 3.7,
            2.3, 3.7, 3.3, 3, 2.7, 4, 3.3, 3.3, 2.3, 2.7, 3.3, 1.7, 3.7],
    "work_experience": [3, 4, 3, 5, 4, 6, 1, 4, 5, 1, 3, 5, 6, 4, 3, 1, 4,
                        6, 2, 3, 2, 1, 4, 1, 2, 6, 4, 2, 6, 5, 1, 2, 4, 6,
                        5, 1, 2, 1, 4, 5],
    "admitted": [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0,
                 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1]
}

x = pd.DataFrame(candidates)
y = x.pop("admitted")

test = SelectKBest(score_func=chi2, k=3)
chi_score = test.fit(x, y)
print(chi_score.scores_)
print(f"Features: {x.columns[chi_score.get_support()]}")

# Re-assign X with significant columns only after chi-square test.
x.pop("gpa")
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

logistic_model = LogisticRegression(fit_intercept=True, solver="liblinear", random_state=0)
logistic_model.fit(X_train, y_train)

with open("model_pkl", "wb") as files:
    pickle.dump(logistic_model, files)

with open("model_pkl", "rb") as f:
    model = pickle.load(f)

predictions = model.predict(X_test)
confusion_metrix = pd.crosstab(
    y_test, predictions, rownames=["Actual"], colnames=["Predicted"]
)
print(confusion_metrix)
print(f"Accuracy: {metrics.accuracy_score(y_test, predictions)}"
      f"\nPrecision: {metrics.precision_score(y_test, predictions)}"
      f"\nRecall: {metrics.recall_score(y_test, predictions)}")

single_prediction = model.predict([[550, 4]])
print(single_prediction)
