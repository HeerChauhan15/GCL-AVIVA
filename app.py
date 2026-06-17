st.header("📂 Upload Member Data for Bulk Rate Lookup")
st.markdown("Your Excel must have at least: **Name, Age, Tenure (in Years)**.")
st.markdown("⚠️ Please make sure you have selected the correct Loan Type before uploading your Excel file.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_rates = pd.read_excel(RATE_FILE, sheet_name=SHEET_NAME)
        df_rates.columns = [str(col).strip() for col in df_rates.columns]
        age_column = df_rates.columns[0]
        df_rates[age_column] = pd.to_numeric(df_rates[age_column], errors="coerce").astype("Int64")

        df_members = pd.read_excel(uploaded_file)
        results = []

        for _, row in df_members.iterrows():
            member_name = row["Name"]
            member_age = int(row["Age"])
            tenure_years = int(row["Tenure"])  # tenure already in years

            if member_age in df_rates[age_column].values:
                rate_row = df_rates[df_rates[age_column] == member_age]
                tenure_column = next((col for col in df_rates.columns if str(tenure_years) in str(col)), None)

                if tenure_column:
                    rate = round(rate_row.iloc[0][tenure_column], 4)
                    premium = round(rate * (row.get("Insure Amount", 50000)) / 50000, 2)
                    results.append([member_name, member_age, tenure_years, rate, premium])
                else:
                    results.append([member_name, member_age, tenure_years, "N/A", "N/A"])
            else:
                results.append([member_name, member_age, tenure_years, "N/A", "N/A"])

        df_results = pd.DataFrame(results, columns=["Name", "Age", "Tenure (Years)", "Rate", "Premium"])
        st.success("Bulk Rates Calculated Successfully")
        st.dataframe(df_results)

    except Exception as e:
        st.error(f"Error: {e}")
