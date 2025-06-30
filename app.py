import streamlit as st
import pandas as pd
import numpy as np
import math

st.title("TSS Calculator")

ftp = st.number_input(
    "Enter your FTP",
    min_value=1,
    max_value=1000,
    step=1,
    format="%d"
)

uploaded_file = st.file_uploader("Upload your workout CSV", type=["csv"])

if ftp and uploaded_file:
    data = pd.read_csv(uploaded_file)

    # --- Auto-detect Power Column ---
    power_keywords = ['power', 'watts', 'output']
    detected_power_col = next(
        (c for c in data.columns if any(k in c.lower() for k in power_keywords)),
        None
    )

    if detected_power_col is None and data.shape[1] >= 1:
        detected_power_col = data.columns[0]
        st.warning(
            f"⚠️ No power header match found — defaulted to first column '{detected_power_col}'. Please verify!"
        )

    # --- User Confirmation for Power Column ---
    st.markdown("### 🛠️ Confirm Power Column")
    power_col = st.selectbox(
        "Select Power Column",
        options=data.columns,
        index=list(data.columns).index(detected_power_col) if detected_power_col in data.columns else 0
    )

    if power_col not in data.columns:
        st.error("Selected power column not found in the data.")
        st.stop()

    # --- Create Time Column: 1 row = 1 second ---
    data['time_seconds'] = np.arange(len(data))

    # --- Compute Rolling Average & TSS ---
    data['Rolling_Avg'] = data[power_col].rolling(window=30).mean()
    data['Rolling_Avg_4th'] = data['Rolling_Avg'] ** 4
    normalized_power = data['Rolling_Avg_4th'].mean() ** 0.25

    duration_seconds = data['time_seconds'].iloc[-1] - data['time_seconds'].iloc[0]
    duration_hours = duration_seconds / 3600
    tss = (normalized_power ** 2 * duration_hours) / (ftp ** 2) * 100

    normalized_power = math.ceil(normalized_power)
    tss = math.ceil(tss)

    # --- Display Results ---
    st.subheader("🚴 Your Workout Summary")
    c1, c2 = st.columns(2)
    c1.metric("Normalized Power (NP)", f"{normalized_power} W")
    c2.metric("Training Stress Score (TSS)", f"{tss}")

    st.markdown("---")
    st.write("### Uploaded Data Preview")
    st.dataframe(data)

elif not ftp:
    st.warning("Please enter a valid FTP value greater than 0.")
elif not uploaded_file:
    st.info("Please upload a CSV workout file to continue.")
