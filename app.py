import streamlit as st
import pandas as pd
import math

# Title of the app
st.title("TSS Calculator")

# User input for FTP
ftp = st.number_input(
    "Enter your FTP",
    min_value=1,
    max_value=1000,
    step=1,
    format="%d",
    key="ftp_input"
)

# Upload CSV file
uploaded_file = st.file_uploader("Upload your workout CSV", type=["csv"])

# Check if FTP and file are provided
if ftp and uploaded_file:
    # Read the CSV
    data = pd.read_csv(uploaded_file)

    # Try to detect power column based on partial match
    power_keywords = ['output', 'power', 'watts']
    detected_power_col = next((col for col in data.columns if any(k in col.lower() for k in power_keywords)), None)

    # Try to detect time column based on partial match
    time_keywords = ['time', 'seconds', 'minutes']
    detected_time_col = next((col for col in data.columns if any(k in col.lower() for k in time_keywords)), None)

    # Fallbacks
    if detected_power_col is None and data.shape[1] >= 2:
        detected_power_col = data.columns[1]
        st.warning(f"No power header match found — defaulting to column '{detected_power_col}'")

    if detected_time_col is None and data.shape[1] >= 1:
        detected_time_col = data.columns[0]
        st.warning(f"No time header match found — defaulting to column '{detected_time_col}'")

    # Let user override detection
    st.markdown("### 🛠️ Confirm or Adjust Columns")
    power_col = st.selectbox("Select Power Column", options=data.columns, index=data.columns.get_loc(detected_power_col) if detected_power_col in data.columns else 0)
    time_col = st.selectbox("Select Time Column", options=data.columns, index=data.columns.get_loc(detected_time_col) if detected_time_col in data.columns else 0)

    # Convert time column to seconds if it's likely in minutes
    if data[time_col].max() < 100:  # heuristic: probably minutes
        data[time_col] = data[time_col] * 60
        data.rename(columns={time_col: "Time (s)"}, inplace=True)
        time_col = "Time (s)"
    elif time_col == "category":
        data.rename(columns={time_col: "Time (s)"}, inplace=True)
        time_col = "Time (s)"

    # Final check for power column
    if power_col not in data.columns:
        st.error("Selected power column not found in the data.")
    else:
        # TSS Calculation Logic
        data['Rolling_Avg'] = data[power_col].rolling(window=30).mean()
        data['Rolling_Avg_4th'] = data['Rolling_Avg'] ** 4
        normalized_power = data['Rolling_Avg_4th'].mean() ** (1/4)

        # Duration in hours from time column
        time_vals = data[time_col]
        duration_seconds = time_vals.iloc[-1] - time_vals.iloc[0]
        duration_hours = duration_seconds / 3600

        tss = (normalized_power ** 2 * duration_hours) / (ftp ** 2) * 100

        # Round up values
        normalized_power = math.ceil(normalized_power)
        tss = math.ceil(tss)

        # Display results at the top of the page
        st.subheader("🚴 Your Workout Summary")
        col1, col2 = st.columns(2)
        col1.metric("Normalized Power (NP)", f"{normalized_power} W")
        col2.metric("Training Stress Score (TSS)", f"{tss}")

        # Separator for detailed data
        st.markdown("---")
        st.write("Uploaded Workout Data:")
        st.dataframe(data)


elif not ftp:
    st.warning("Please enter a valid FTP value greater than 0.")
elif not uploaded_file:
    st.info("Please upload a valid workout CSV file from domestiq.net to proceed.")
