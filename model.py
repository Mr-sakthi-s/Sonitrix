import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
import joblib

# Load datasets
hard = pd.read_csv("rich_features_label_0.csv")
soft = pd.read_csv("rich_features_label_1.csv")

data = pd.concat([hard, soft], ignore_index=True)

X = data[["mean","std","range","jitter","loss_rate"]]
y = data["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Train model
model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3
)

model.fit(X_train, y_train)

# Evaluate
print("\nModel Evaluation:\n")
print(classification_report(y_test, model.predict(X_test)))

# Save model
joblib.dump(model, "hard_soft_model.pkl")
print("\nModel saved as hard_soft_model.pkl")
