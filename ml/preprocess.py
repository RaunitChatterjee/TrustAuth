import pandas as pd


DATASET_PATH = "ml/dataset/DSL-StrongPasswordData.csv"


def load_dataset():
    """
    Load the keystroke dynamics dataset.
    """

    print("=" * 60)
    print("Loading dataset...")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)

    print("Dataset loaded successfully.\n")

    return df


def inspect_dataset(df):
    """
    Display basic dataset information.
    """

    print("=" * 60)
    print("Dataset Shape")
    print("=" * 60)

    print(df.shape)

    print("\n")

    print("=" * 60)
    print("Columns")
    print("=" * 60)

    print(list(df.columns))

    print("\n")

    print("=" * 60)
    print("First 5 Rows")
    print("=" * 60)

    print(df.head())

    print("\n")

    print("=" * 60)
    print("Missing Values")
    print("=" * 60)

    print(df.isnull().sum())

    print("\n")

    print("=" * 60)
    print("Unique Users")
    print("=" * 60)

    print(df["subject"].nunique())

    print("\n")

    print("=" * 60)
    print("Samples Per User")
    print("=" * 60)

    print(df.groupby("subject").size())


def main():

    df = load_dataset()

    inspect_dataset(df)


if __name__ == "__main__":
    main()