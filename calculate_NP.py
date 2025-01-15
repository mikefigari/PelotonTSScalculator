import pandas as pd
import os

def read_ftp(file_name="ftp.txt"):
    """
    Read FTP value from a static file.
    
    Args:
        file_name (str): Path to the FTP file.
    
    Returns:
        float: FTP value.
    """
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return float(file.read().strip())
    else:
        print(f"No FTP file found. Creating a new one at {file_name}.")
        new_ftp = float(input("Enter your FTP value to save: "))
        with open(file_name, "w") as file:
            file.write(str(new_ftp))
        return new_ftp


def calculate_normalized_power_and_tss(file_path, ftp):
    """
    Calculate Normalized Power (NP) and Training Stress Score (TSS) from a workout dataset.
    
    Args:
        file_path (str): Path to the CSV file with workout data.
        ftp (float): Functional Threshold Power.
    
    Returns:
        tuple: Normalized Power (NP) and Training Stress Score (TSS).
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)
        
        # Ensure required columns exist
        if 'category' not in data.columns or 'Output - Workout' not in data.columns:
            raise ValueError("Dataset must contain 'category' and 'Output - Workout' columns.")
        
        # Convert time from minutes to seconds
        data['Time (seconds)'] = data['category'] * 60  # Convert minutes to seconds
        
        # Step 1: Calculate 30-second rolling average
        data['30s_Rolling_Avg'] = data['Output - Workout'].rolling(window=30, min_periods=1).mean()
        
        # Step 2: Raise each rolling average to the fourth power
        data['Rolling_Avg_Power^4'] = data['30s_Rolling_Avg'] ** 4
        
        # Step 3: Calculate the mean of these fourth powers
        mean_power_4 = data['Rolling_Avg_Power^4'].mean()
        
        # Step 4: Take the fourth root of the mean to get NP
        normalized_power = mean_power_4 ** 0.25
        
        # Calculate Total Duration (hours)
        total_duration_minutes = data['category'].max()
        total_duration_hours = total_duration_minutes / 60  # Convert to hours
        
        # Calculate Intensity Factor (IF)
        intensity_factor = normalized_power / ftp
        
        # Calculate TSS
        tss = (normalized_power * intensity_factor * total_duration_hours / ftp) ** 2 * 100
        
        return normalized_power, tss
    
    except Exception as e:
        print(f"Error: {e}")
        return None, None


if __name__ == "__main__":
    # Read FTP value from file or prompt for it
    ftp = read_ftp()
    
    # Get the workout CSV file path from the user
    file_path = input("Enter the path to your CSV file: ")
    
    # Calculate NP and TSS
    np, tss = calculate_normalized_power_and_tss(file_path, ftp)
    
    if np and tss:
        print(f"Functional Threshold Power (FTP): {ftp:.2f} watts")
        print(f"Normalized Power (NP): {np:.2f} watts")
        print(f"Training Stress Score (TSS): {tss:.2f}")
