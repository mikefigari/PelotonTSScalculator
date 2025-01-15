import streamlit as st
import pandas as pd

# Title of the web app
st.title("TSS Calculator")

# User input for FTP
ftp = st.number_input("Enter your FTP", min_value=1, max_value=1000, value=217, step=1)

# Upload CSV file
uploaded_file = st.file_uploader("Upload your workout CSV", type=["csv"])

import math

if uploaded_file:
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
    
    # Add a separator for the detailed data below
    st.markdown("---")

    # Display the uploaded data
    st.write("Uploaded Workout Data:")
    st.dataframe(data)
