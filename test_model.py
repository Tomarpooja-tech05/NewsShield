import pandas as pd
import joblib
import json

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset"

print("\n========== NEWSHIELD AUTOMATED TESTING ==========\n")

# Load trained model
model = joblib.load(BASE_DIR / "news_model.pkl")

print("Trained model loaded successfully!")

# Load datasets
fake = pd.read_csv(DATA_DIR / "Fake.csv")
real = pd.read_csv(DATA_DIR / "True.csv")

# Assign labels
fake["label"] = 0
real["label"] = 1

# Combine datasets
data = pd.concat([fake, real], ignore_index=True)

# Prepare news content
data["title"] = data["title"].fillna("")
data["text"] = data["text"].fillna("")

data["content"] = (
    data["title"].astype(str) + " " +
    data["text"].astype(str)
).str.strip()

# Remove empty and duplicate articles
data = data[data["content"].str.len() > 20]
data = data.drop_duplicates(subset=["content"])

X = data["content"]
y = data["label"]

print(f"Total articles: {len(data)}")

# Recreate original test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Testing articles: {len(X_test)}")

# Predict using saved model
predictions = model.predict(X_test)

# Calculate performance
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)

correct = (predictions == y_test).sum()
wrong = len(y_test) - correct

# Display results
print("\n========== NEWSHIELD TEST RESULTS ==========")

print(f"Total Tested: {len(X_test)}")
print(f"Correct Predictions: {correct}")
print(f"Wrong Predictions: {wrong}")

print(f"\nAccuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Fake News", "Real News"],
    zero_division=0
))
cm = confusion_matrix(y_test, predictions)

# Save testing results
results = {
    "total_tested": int(len(X_test)),
    "correct_predictions": int(correct),
    "wrong_predictions": int(wrong),
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "confusion_matrix": cm.tolist()
}

with open(BASE_DIR / "test_metrics.json", "w") as file:
    json.dump(results, file, indent=4)

print("\nTesting report saved successfully!")
print("File: test_metrics.json")
print("\n========== TESTING COMPLETED ==========\n")