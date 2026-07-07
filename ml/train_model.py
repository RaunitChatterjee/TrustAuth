import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from feature_engineering import build_feature_vector, load_dataset


MODEL_PATH = "ml/saved_model/random_forest_model.joblib"
ENCODER_PATH = "ml/saved_model/label_encoder.joblib"


def prepare_data():

    df = load_dataset()

    features = build_feature_vector(df)

    X = features.drop(columns=["subject"])

    y = features["subject"]

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(y)

    return X, y_encoded, encoder


def train():

    X, y, encoder = prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("=" * 60)
    print("Model Accuracy")
    print("=" * 60)
    print(f"{accuracy * 100:.2f}%")

    print("\n")

    print("=" * 60)
    print("Classification Report")
    print("=" * 60)
    print(classification_report(y_test, predictions))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)

    print("\nModel saved successfully.")


if __name__ == "__main__":
    train()