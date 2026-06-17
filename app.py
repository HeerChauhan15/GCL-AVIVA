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

# ============================================
# FILE PATH
# ============================================

RATE_FILE = "Homeloan.xlsx"   # your actual file name

# ============================================
# SHEET DROPDOWN (auto-detect)
# ============================================

try:
    sheet_names = pd.ExcelFile(RATE_FILE).sheet_names
    loan_type = st.selectbox("Select Loan Type (Sheet)", sheet_names)
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

# ============================================
# MANUAL RATE LOOKUP
# ============================================

st.header("🔎 Manual Rate Lookup")

age = st.number_input("Age", min_value=18, max_value=65, step=1)
tenure = st.number_input("Tenure (in Years)", min_value=2, step=1)

if st.button("Get Rates"):
    try:
        df = pd.read_excel(RATE_FILE, sheet_name=loan_type)
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
st.markdown("Upload an Excel file with columns: **Name, Age, Insure Amount**")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_rates = pd.read_excel(RATE_FILE, sheet_name=loan_type)
        df_rates.columns = [str(col).strip() for col in df_rates.columns]
        age_column = df_rates.columns[0]
        df_rates[age_column] = pd.to_numeric(df_rates[age_column], errors="coerce").astype("Int64")

        df_members = pd.read_excel(uploaded_file)
        results = []

        for _, row in df_members.iterrows():
            member_name = row["Name"]
            member_age = int(row["Age"])
            insure_amount = row["Insure Amount"]

            if member_age in df_rates[age_column].values:
                rate_row = df_rates[df_rates[age_column] == member_age]
                tenure_column = df_rates.columns[1]  # default: first tenure column
                rate = round(rate_row.iloc[0][tenure_column], 4)
                premium = round(rate * insure_amount / 50000, 2)
                results.append([member_name, member_age, insure_amount, rate, premium])
            else:
                results.append([member_name, member_age, insure_amount, "N/A", "N/A"])

        df_results = pd.DataFrame(results, columns=["Name", "Age", "Insure Amount", "Rate", "Premium"])
        st.success("Bulk Rates Calculated Successfully")
        st.dataframe(df_results)

    except Exception as e:
        st.error(f"Error: {e}")







