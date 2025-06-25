import streamlit as st
import pandas as pd
import numpy as np
import math

# Utility to normalize various time formats into elapsed seconds
def normalize_time_column(df, time_col):
    # 1) Try parsing as ISO datetimes
    try:
        dt = pd.to_datetime(df[time_col], errors='raise')
        df['time_seconds'] = (dt - dt.min()).dt.total_seconds()
        return df
    except Exception:
        pass

    # 2) Try numeric conversion (string→float, or already numeric)
    df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
    if df[time_col].notna().all():
        maxv = df[time_col].max()
        # <=100 → probably minutes
        if maxv <= 100:
            df['time_seconds'] = df[time_col] * 60
        else:
            df['time_seconds'] = df[time_col]
        return df

    # 3) Try colon-delimited HH:MM:SS or MM:SS
    sample = str(df[time_col].dropna().iloc[0])
    if ':' in sample:
        parts = df[time_col].astype(str).str.split(':')
        def to_secs(p):
            nums = [float(x) for x in p]
            if len(nums) == 2:
                return nums[0] * 60 + nums[1]
            elif len(nums) == 3:
                return nums[0] * 3600 + nums[1] * 60 + nums[2]
            else:
                raise ValueError(f"Cannot parse time segment: {p}")
        df['time_seconds'] = parts.apply(to_secs)
        return df

    # If we get here, nothing matched
    raise ValueError(f"Unrecognized time format in column '{time_col}'")


# --- Streamlit app layout ---
st.title("TSS Calculator")

ftp = st.number_input(
    "Enter your FTP",
    min_value=1, max_value=1000, step=1,
    format="%d", key="ftp_input"
)

uploaded_file = st.file_uploader("Upload your workout CSV", type=["csv"])


if ftp and uploaded_file:
    # 1) Load data
    data = pd.read_csv(uploaded_file)

    # 2) Auto-detect power column
    power_keywords = ['output', 'power', 'watts']
    detected_power_col = next(
        (c for c in data.columns if any(k in c.lower() for k in power_keywords)),
        None
    )
    if not detected_power_col and data.shape[1] >= 2:
        detected_power_col = data.columns[1]
        st.warning(f"No power header match—defaulting to '{detected_power_col}'")

    # 3) Auto-detect time column
    time_keywords = ['time', 'seconds', 'minutes']
    detected_time_col = next(
        (c for c in data.columns if any(k in c.lower() for k in time_keywords)),
        None
    )
    if not detected_time_col and data.shape[1] >= 1:
        detected_time_col = data.columns[0]
        st.warning(f"No time header match—defaulting to '{detected_time_col}'")

    # 4) Let user confirm or override
    st.markdown("### 🛠️ Confirm or Adjust Columns")
    power_col = st.selectbox(
        "Select Power Column",
        options=data.columns,
        index=list(data.columns).index(detected_power_col) if detected_power_col in data.columns else 0
    )
    time_col = st.selectbox(
        "Select Time Column",
        options=data.columns,
        index=list(data.columns).index(detected_time_col) if detected_time_col in data.columns else 0
    )

    # 5) Normalize the time into elapsed seconds
    try:
        data = normalize_time_column(data, time_col)
    except Exception as e:
        st.error(f"Error parsing your time column: {e}")
        st.stop()

    # 6) Ensure the power column exists
    if power_col not in data.columns:
        st.error("Selected power column not found in the data.")
        st.stop()

    # 7) Compute rolling average, normalized power & TSS
    data['Rolling_Avg'] = data[power_col].rolling(window=30).mean()
    data['Rolling_Avg_4th'] = data['Rolling_Avg'] ** 4
    normalized_power = data['Rolling_Avg_4th'].mean() ** 0.25

    duration_seconds = data['time_seconds'].iloc[-1] - data['time_seconds'].iloc[0]
    duration_hours = duration_seconds / 3600
    tss = (normalized_power ** 2 * duration_hours) / (ftp ** 2) * 100

    # Round up for display
    normalized_power = math.ceil(normalized_power)
    tss = math.ceil(tss)

    # 8) Show results
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
