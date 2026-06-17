import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Aviva Rate Calculator",
    page_icon="📊",
    layout="centered"
)

# ============================================
# TITLE
# ============================================

st.title("📊 Aviva Rate Calculator")

st.markdown(
    "Select Age and Tenure to fetch the applicable rate. "
    "Sum Assured is fixed at **₹50,000**."
)

# ============================================
# FILE PATH
# ============================================

RATE_FILE = "Homeloan.xlsx"   # your actual file name

# ============================================
# INPUTS
# ============================================

age = st.number_input(
    "Age",
    min_value=18,
    max_value=65,
    step=1
)

st.markdown("**Tenure (in Years)**")

tenure = st.number_input(
    "Tenure",
    min_value=2,
    step=1
)

# ============================================
# CALCULATE BUTTON
# ============================================

if st.button("Get Rate"):

    try:
        # ============================================
        # READ SHEET
        # ============================================

        df = pd.read_excel(
            RATE_FILE,
            sheet_name="Home Loan"   # must match sheet tab name
        )

        # ============================================
        # CLEAN DATA
        # ============================================

        df.columns = [str(col).strip() for col in df.columns]

        # First column assumed to be AGE
        age_column = df.columns[0]

        df[age_column] = pd.to_numeric(
            df[age_column],
            errors="coerce"
        ).astype("Int64")

        # ============================================
        # AGE VALIDATION
        # ============================================

        if age not in df[age_column].values:
            st.error("Age/Tenure not available in rate card.")

        else:
            row = df[df[age_column] == age]

            # Try to match tenure column flexibly
            tenure_column = next(
                (col for col in df.columns if str(tenure) in str(col)),
                None
            )

            # ============================================
            # TENURE VALIDATION
            # ============================================

            if tenure_column is None:
                st.error("Age/Tenure not available in rate card.")
            else:
                rate = row.iloc[0][tenure_column]

                # Round to 4 decimal places
                rate = round(rate, 4)

                st.success("Rate Found Successfully")

                st.metric(
                    label=f"Applicable Rate (Sum Assured ₹50,000)",
                    value=f"₹{rate}"
                )

    except Exception as e:
        st.error(f"Error: {e}")
