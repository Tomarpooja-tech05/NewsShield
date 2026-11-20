import pandas as pd
import joblib
import json

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset"

print("Loading NewsShield dataset...")

fake = pd.read_csv(DATA_DIR / "Fake.csv")
real = pd.read_csv(DATA_DIR / "True.csv")

fake["label"] = 0
real["label"] = 1

data = pd.concat([fake, real], ignore_index=True)

# Combine headline and article text
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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# TF-IDF + Logistic Regression
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_features=100000,
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        random_state=42
    ))
])

print("Training machine learning model...")

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)

# Save trained model
joblib.dump(model, BASE_DIR / "news_model.pkl")

# Save evaluation metrics
metrics = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "total_articles": len(data)
}

with open(BASE_DIR / "metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)

print("\n========== NEWSHIELD RESULTS ==========")
print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1 Score:  {f1 * 100:.2f}%")
print("\nModel saved successfully!")
print("=======================================")