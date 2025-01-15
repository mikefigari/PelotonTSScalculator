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

    # TSS Calculation Logic
    data['Rolling_Avg'] = data['Output - Workout'].rolling(window=30).mean()
    data['Rolling_Avg_4th'] = data['Rolling_Avg'] ** 4
    normalized_power = data['Rolling_Avg_4th'].mean() ** (1/4)
    duration_hours = len(data) / 3600
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
