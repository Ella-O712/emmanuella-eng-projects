## Overview

The script is designed to be versatile and can handle multiple CSV datasets, providing flexible data processing, statistical analysis, and visualization.

### Key Operations:
- **Loading and Summarizing Data**: The script reads the dataset and provides summary statistics for numerical columns.
- **Data Filtering**: Rows are filtered based on conditions such as `Value > 50`, but this can be easily modified in the script.
- **Group Aggregation**: Data is grouped by `Industry`, and the mean `Value` is calculated for each group.
- **Visualization**: A pair plot is generated using Seaborn to explore relationships between different columns in the dataset.

## Dataset Information

The dataset used in this project relates to work-related injury statistics and includes the following columns:

- **Year**: The year of the injury claim.
- **Sex**: The sex of the individual.
- **Age group**: The age group of the individual at the time of the injury.
- **Geographic region**: The region where the injury occurred.
- **Employment status**: The employment status of the individual.
- **Occupation**: The occupation of the injured individual.
- **Injury/illness group**: Group or classification of the injury or illness.
- **Type of injury**: The specific type of injury or illness.
- **Industry**: The industry sector where the injury occurred.
- **Value**: A numeric representation of injury claims or measures.
- **Measure**: Type of measure (e.g., count, percentage).
- **Status**: Status of the claim or measure.

## Project Structure

The project is organized as follows:

- **Python Script (`main.py`)**: The main script that performs the data processing operations such as loading, filtering, grouping, and visualizing the data.
- **Processed Data**: The processed CSV files generated after running the script will be saved in the same directory as the original dataset.
- **Visualizations**: Pair plots are generated automatically to assist with exploratory data analysis.
