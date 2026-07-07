import pandas as pd
import numpy as np


DATASET_PATH = "ml/dataset/DSL-StrongPasswordData.csv"


def load_dataset():
    return pd.read_csv(DATASET_PATH)


def split_columns(df):
    """
    Separate Hold Time and Flight Time columns.
    """

    hold_columns = [
        column
        for column in df.columns
        if column.startswith("H.")
    ]

    flight_columns = [
        column
        for column in df.columns
        if column.startswith("UD.")
    ]

    return hold_columns, flight_columns


def build_feature_vector(df):

    hold_columns, flight_columns = split_columns(df)

    features = pd.DataFrame()

    features["subject"] = df["subject"]

    # Hold time features
    features["avg_hold_time"] = df[hold_columns].mean(axis=1)
    features["hold_std"] = df[hold_columns].std(axis=1)
    features["hold_variance"] = df[hold_columns].var(axis=1)
    features["min_hold_time"] = df[hold_columns].min(axis=1)
    features["max_hold_time"] = df[hold_columns].max(axis=1)

    # Flight time features
    features["avg_flight_time"] = df[flight_columns].mean(axis=1)
    features["flight_std"] = df[flight_columns].std(axis=1)
    features["flight_variance"] = df[flight_columns].var(axis=1)
    features["min_flight_time"] = df[flight_columns].min(axis=1)
    features["max_flight_time"] = df[flight_columns].max(axis=1)

    return features


def main():

    df = load_dataset()

    features = build_feature_vector(df)

    print("=" * 60)
    print("Generated Feature Vector")
    print("=" * 60)

    print(features.head())

    print("\n")

    print("=" * 60)
    print("Feature Shape")
    print("=" * 60)

    print(features.shape)


if __name__ == "__main__":
    main()