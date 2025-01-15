import pandas as pd

def calculate_normalized_power(file_path):
    """
    Calculate Normalized Power (NP) from a dataset with specified column headers.

    Args:
        file_path (str): Path to the CSV file with workout data.
        
    Returns:
        float: Normalized Power (NP).
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)
        
        # Ensure required columns exist
        if 'category' not in data.columns or 'Output - Workout' not in data.columns:
            raise ValueError("Dataset must contain 'category' (Time in minutes) and 'Output - Workout' (Watts) columns.")
        
        # Rename columns for processing
        data.rename(columns={'category': 'Time', 'Output - Workout': 'Output - Watts'}, inplace=True)
        
        # Convert time from minutes to seconds
        data['Time (seconds)'] = data['Time'] * 60  # Convert minutes to seconds
        
        # Step 1: Calculate 30-second rolling average
        data['30s_Rolling_Avg'] = data['Output - Watts'].rolling(window=30, min_periods=1).mean()
        
        # Step 2: Raise each rolling average to the fourth power
        data['Rolling_Avg_Power^4'] = data['30s_Rolling_Avg'] ** 4
        
        # Step 3: Calculate the mean of these fourth powers
        mean_power_4 = data['Rolling_Avg_Power^4'].mean()
        
        # Step 4: Take the fourth root of the mean to get NP
        normalized_power = mean_power_4 ** 0.25
        
        return normalized_power
    
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    file_path = input("Enter the path to your CSV file: ")  # Prompt user for file path
    np = calculate_normalized_power(file_path)
    if np:
        print(f"Normalized Power (NP): {np:.2f} watts")
