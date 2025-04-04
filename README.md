# TSS Calculator

Welcome to the TSS Calculator repository! This tool helps you calculate your Training Stress Score (TSS) from your cycling workout data. By using this script, you can input your FTP (Functional Threshold Power) and workout data to generate accurate TSS results. Follow the instructions below to get started.

## 🌐 Live App

👉 [tsscalculator.michaelfigari.com](https://tsscalculator.michaelfigari.com)

No setup required — just open the site, enter your FTP, and upload your workout CSV.

## Prerequisites

- Python 3.x installed on your system.
- Basic knowledge of running Python scripts.
- A text file (`ftp.txt`) to store your FTP value.
- A CSV file containing your workout data.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/<repository-name>.git
   cd <repository-name>
   ```

2. **Install Dependencies** (if any):
   - This script currently does not use any external Python libraries.
   - If additional libraries are required in the future, they will be listed here.

## How to Use

1. **Enter Your FTP**:
   - Open the `ftp.txt` file in a text editor.
   - Enter your FTP (e.g., `200`) and save the file.

2. **Prepare Your Workout Data**:
   - Copy and paste your workout data from [Domestiq](https://domestiq.net/) into a file named `workout.csv`.
   - Alternatively, rename the file containing your workout data to `workout.csv`.
   - Ensure the data follows this format:
     ```csv
     category,Output - Workout
     0,27
     0.016666666666666666,29
     0.03333333333333333,31
     ...
     ```
     - **category**: Time in minutes (fractional).
     - **Output - Workout**: Wattage recorded at each second.

3. **Run the Script**:
   - Open a terminal in the project directory.
   - Execute the script:
     ```bash
     python calculate_TSS.py
     ```

4. **View Results**:
   - The script will calculate and display the following:
     - **Normalized Power (NP):** Average power adjusted for intensity.
     - **TSS:** Training Stress Score for the workout.

## Notes

- Ensure the `workout.csv` file is in the same directory as the script.
- The script assumes each row in the CSV represents one second of workout data.
- The TSS calculation assumes the total duration of the workout is the number of rows divided by 60 (to convert seconds to minutes) and further divided by 60 (to convert minutes to hours).

## Troubleshooting

- **Incorrect TSS Value**: Ensure the FTP in `ftp.txt` is correct and the CSV data is formatted properly.
- **Script Error**: Double-check that the Python script and required files are in the same directory.

## Contributing

Contributions to improve this script or add features are welcome! Feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Questions or Feedback?

If you have any questions or feedback, feel free to open an issue on GitHub.

