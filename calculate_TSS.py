import pandas as pd
import numpy as np

# File path for your workout data
file_path = 'workout.csv'  # Make sure workout.csv is in the same directory as the script

# Load the CSV data
data = pd.read_csv(file_path)

# Step 1: Read FTP value
with open('ftp.txt', 'r') as ftp_file:
    ftp = float(ftp_file.read().strip())

# Step 2: Calculate rolling average (window size in seconds)
window_size = 30
data['Rolling_Avg'] = data['Output - Workout'].rolling(window=window_size).mean()

# Step 3: Calculate the 4th power of the rolling average
data['Rolling_Avg_4th'] = data['Rolling_Avg'] ** 4

# Step 4: Calculate Normalized Power (NP)
normalized_power = data['Rolling_Avg_4th'].mean() ** (1/4)

# Step 5: Calculate total duration in HOURS (each row = 1 second)
duration_hours = len(data) / 3600

# Step 6: Calculate TSS
tss = (normalized_power ** 2 * duration_hours) / (ftp ** 2) * 100

print(f"Normalized Power (NP): {normalized_power:.2f} W")
print(f"Total TSS: {tss:.2f}")
