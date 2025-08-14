import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def process_dataset(file_path, output_file=None):
    """
    Loads and processes a dataset from a CSV file, performing basic
    operations like filtering, grouping, and visualization.

    Args:
        file_path (str): Path to the CSV file.
        output_file (str, optional): Path to save the processed data. Defaults to None.

    Returns:
        pd.DataFrame: The processed dataset.
    """

    # Check if file exists before proceeding
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
        return None

    try:
        # Load the dataset (using ISO-8859-1 encoding as the file may have special characters)
        print(f"Loading dataset from '{file_path}'...")
        data = pd.read_csv(file_path, encoding='ISO-8859-1')
    except Exception as e:
        # Handle any errors that might come up when loading the file
        print(f"An error occurred while reading the file: {e}")
        return None

    # Display basic info about the dataset
    print("\n--- Dataset Overview ---")
    print(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
    print("Column Names:", data.columns.tolist())

    # Display summary statistics for numerical columns
    print("\n--- Summary Statistics ---")
    print(data.describe())

    # Check if expected columns are present for filtering and grouping
    if "Value" not in data.columns or "Industry" not in data.columns:
        print("\nError: Required columns 'Value' or 'Industry' are missing in the dataset.")
        return None

    # Filter the data: Example - selecting rows where 'Value' > 50
    print("\nFiltering rows where 'Value' > 50...")
    filtered_data = data[data["Value"] > 50]
    print(f"Filtered data contains {filtered_data.shape[0]} rows after filtering.")

    # Group the data by 'Industry' and calculate the mean 'Value'
    print("\nCalculating mean 'Value' per 'Industry'...")
    grouped_data = data.groupby("Industry")["Value"].mean()
    print(grouped_data)

    # Visualize the dataset (pairplot example)
    try:
        print("\nGenerating pairplot for the dataset...")
        sns.pairplot(data)
        plt.suptitle(f"Pairplot of {file_path}", y=1.02)
        plt.show()
    except Exception as e:
        print(f"An error occurred while generating the pairplot: {e}")

    # Save the processed dataset if output file path is provided
    if output_file:
        try:
            print(f"\nSaving processed data to '{output_file}'...")
            data.to_csv(output_file, index=False)
            print("File saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")

    return data


# Main section of the script
if __name__ == "__main__":
    # File path for the dataset (ensure this is in the same directory or provide full path)
    file_path = 'injury-statistics-work-related-claims-2018-csv.csv'

    # Output file path for saving processed data
    output_file = 'processed_injury_statistics.csv'

    # Call the processing function
    processed_data = process_dataset(file_path, output_file)

    # Print final message based on success or failure
    if processed_data is not None:
        print("\nData processing completed successfully!")
    else:
        print("\nData processing failed.")
