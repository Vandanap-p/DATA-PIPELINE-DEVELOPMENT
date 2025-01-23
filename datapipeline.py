import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# Step 1: Data Loading
def load_data(file_path):
    """Load data from a CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path, on_bad_lines='skip')  # Skip bad lines
        print("Data loaded successfully.")
        print("Data Shape:", data.shape)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Step 2: Data Preprocessing
def preprocess_data(df, categorical_columns, target_column):
    """Preprocess the data by handling missing values and encoding categorical variables."""
    df = df.copy()

    # Handle missing values
    df.fillna(df.median(numeric_only=True), inplace=True)
    df.fillna("Unknown", inplace=True)

    # Encode categorical columns
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    return X, y, label_encoders

# Step 3: Data Transformation
def transform_data(X, scaling_columns):
    """Standardize the data for specified columns."""
    if scaling_columns:
        scaler = StandardScaler()
        X[scaling_columns] = scaler.fit_transform(X[scaling_columns])
        return X, scaler
    else:
        print("No scaling columns specified or found.")
        return X, None

# Step 4: Train-Test Split
def split_data(X, y, test_size=0.2, random_state=42):
    """Split the data into training and testing sets."""
    if len(X) <= 1:
        print("Not enough samples to split.")
        return None, None, None, None
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# Step 5: Main Pipeline
def data_pipeline(file_path, categorical_columns, scaling_columns, target_column):
    """End-to-end data pipeline for loading, preprocessing, transforming, and splitting data."""
    # Load data
    data = load_data(file_path)
    if data is None:
        return None, None, None, None

    # Preprocess data
    X, y, label_encoders = preprocess_data(data, categorical_columns, target_column)

    # Transform data
    X, scaler = transform_data(X, scaling_columns)

    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    if X_train is None:
        return None, None, None, None

    print("Pipeline executed successfully.")
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Define parameters
    file_path = 'customer_data.csv'  # Path to your dataset
    categorical_columns = ["CustomerID", "Gender", "Country", "PurchaseDate"]  # Replace with the actual categorical column names
    scaling_columns = ["Age", "PurchaseAmount"]  # Replace with the actual numerical column names
    target_column = "PurchaseDate"  # Replace with your target column name

    # Run the pipeline
    X_train, X_test, y_train, y_test = data_pipeline(file_path, categorical_columns, scaling_columns, target_column)

    # Example output
    if X_train is not None:
        print("Training set size:", X_train.shape)
        print("Test set size:", X_test.shape)
