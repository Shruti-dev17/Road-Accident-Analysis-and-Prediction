import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib


df= pd.read_csv(r"F:\Desktop\code\Road Accident Analysis And Prediction\data_ML.csv")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")
df = df.drop(columns=["Time of Day"], errors="ignore")

X = df.drop("Accident Severity", axis=1)
y = df["Accident Severity"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(y_pred[:10])



print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


cm = confusion_matrix(y_test, y_pred)
joblib.dump(cm, "models/confusion_matrix.pkl")
joblib.dump(model.classes_.tolist(), "models/class_labels.pkl")


sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Accident Severity")
plt.show()

joblib.dump(model, "models/accident_severity_model.pkl")
feature_names = X.columns.tolist()

joblib.dump(feature_names, "models/feature_names.pkl")

print("Model saved successfully!")
print("Feature names saved successfully!")


importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
).head(10)

print("\nTop 10 Important Features:")
print(importance)

importance.to_csv(
    r"F:\Desktop\code\Road Accident Analysis And Prediction\models\feature_importance.csv",
    index=False
)


plt.figure(figsize=(10, 6))

sns.barplot(
    data=importance,
    x="Importance",
    y="Feature"
)

plt.title("Top 10 Features for Accident Severity Prediction")
plt.tight_layout()
plt.show()

print("Feature importance saved successfully!")