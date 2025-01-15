ftp = st.number_input(
    "Enter your FTP",
    min_value=1,
    max_value=1000,
    value=None,
    step=1,
    format="%d",
    key="ftp_input"
)

if ftp:
    # Proceed only if FTP is entered
    if uploaded_file:
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
        
        st.markdown("---")
        st.write("Uploaded Workout Data:")
        st.dataframe(data)
else:
    st.warning("Please enter your FTP to calculate the results.")
