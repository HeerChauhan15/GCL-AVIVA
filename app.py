import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Aviva GCL Insurance Premium Calculator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Aviva GCL Insurance Premium Calculator")

st.markdown(
    "Select Age and Tenure to fetch the applicable rate. "
    "Sum Assured is fixed at **₹50,000**."
)

# ============================================
# FILE PATH
# ============================================

RATE_FILE = "Homeloan.xlsx"   # your actual file name
SHEET_NAME = "Home Loan"      # your only sheet

# ============================================
# MANUAL RATE LOOKUP
# ============================================

st.header("🔎 Manual Rate Lookup")

age = st.number_input("Age", min_value=18, max_value=65, step=1)
tenure = st.number_input("Tenure (in Years)", min_value=2, step=1)

if st.button("Get Rates"):
    try:
        df = pd.read_excel(RATE_FILE, sheet_name=SHEET_NAME)
        df.columns = [str(col).strip() for col in df.columns]
        age_column = df.columns[0]
        df[age_column] = pd.to_numeric(df[age_column], errors="coerce").astype("Int64")

        if age not in df[age_column].values:
            st.error("Age/Tenure not available in rate card.")
        else:
            row = df[df[age_column] == age]
            tenure_column = next((col for col in df.columns if str(tenure) in str(col)), None)

            if tenure_column is None:
                st.error("Age/Tenure not available in rate card.")
            else:
                rate = round(row.iloc[0][tenure_column], 4)
                st.success("Rate Found Successfully")
                st.metric(label=f"Applicable Rate (Sum Assured ₹50,000)", value=f"₹{rate}")
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================
# BULK RATE LOOKUP
# ============================================

st.header("📂 Upload Member Data for Bulk Rate Lookup")
st.markdown("Your Excel must have at least: **Name, Age, Tenure (in Years)**.")


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
                    results.append([member_name, member_age, tenure_years, premium])
                else:
                    results.append([member_name, member_age, tenure_years, "N/A"])
            else:
                results.append([member_name, member_age, tenure_years, "N/A"])

        df_results = pd.DataFrame(results, columns=["Name", "Age", "Tenure (Years)", "Premium"])
        st.success("Bulk Premiums Calculated Successfully")
        st.dataframe(df_results)

    except Exception as e:
        st.error(f"Error: {e}")
