import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample Data
data = {
    'Class': ['A', 'B', 'C'],
    'Initial Balance ($)': [500_000_000, 30_670_000, 30_670_000],
    'Interest Rate (%)': [5.05, 5.23, 5.47],
    'Maturity Date': ['Sep 20, 2029', 'Sep 20, 2029', 'Sep 20, 2029'],
    'Fitch Rating': ['AAA (sf)', 'AA (sf)', 'A (sf)'],
    "Moody’s Rating": ['Aaa (sf)', 'Aa1 (sf)', 'Aa3 (sf)'],
    'Credit Enhancement (%)': [30.0, 20.0, 10.0]
}
df = pd.DataFrame(data)

# Streamlit UI
st.title("ABS IntelliScan - TMUST 2024-1 Analysis")

st.subheader("Tranche Overview")
st.dataframe(df)

st.subheader("Credit Enhancement by Tranche")
fig, ax = plt.subplots()
ax.bar(df['Class'], df['Credit Enhancement (%)'], color='skyblue')
ax.set_ylabel('Credit Enhancement (%)')
ax.set_xlabel('Tranche Class')
st.pyplot(fig)

st.subheader("AI-Like Observations")
if df['Credit Enhancement (%)'].iloc[2] < 15:
    st.write("- Class C has relatively low enhancement for its A rating.")
if df['Interest Rate (%)'].iloc[2] > df['Interest Rate (%)'].iloc[0]:
    st.write("- Class C offers the highest interest rate, suggesting higher risk.")

import fitz  # PyMuPDF

st.sidebar.title("Upload ABS Offering Memo")
uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()
    
    st.subheader("Extracted Document Preview")
    st.text_area("Raw Text", extracted_text[:3000], height=300)
import re

def extract_tranche_table(text):
    # Clean line breaks and merge broken lines
    text = text.replace("\n", " ")
    pattern = r"Class\s([ABC])\snotes\s.*?\$\s*([\d,]+)\s+(\d+\.\d+)%"
    matches = re.findall(pattern, text)

    if not matches:
        return None

    data = []
    for cls, amount, rate in matches:
        data.append({
            'Class': cls,
            'Initial Balance ($)': int(amount.replace(",", "")),
            'Interest Rate (%)': float(rate)
        })
    return pd.DataFrame(data)


# Extract and display table if file is uploaded
if uploaded_file is not None:
    df_tranches = extract_tranche_table(extracted_text)
    
    if df_tranches is not None:
        st.subheader("Extracted Tranche Table")
        st.dataframe(df_tranches)
        # ✅ AI-Generated Observations
        st.subheader("AI-Generated Observations")

        insights = []

        max_rate_row = df_tranches.loc[df_tranches['Interest Rate (%)'].idxmax()]
        min_rate_row = df_tranches.loc[df_tranches['Interest Rate (%)'].idxmin()]
        
        insights.append(f"- Class {max_rate_row['Class']} has the **highest interest rate** at {max_rate_row['Interest Rate (%)']}%, suggesting **higher risk or subordination**.")
        insights.append(f"- Class {min_rate_row['Class']} has the **lowest interest rate** at {min_rate_row['Interest Rate (%)']}%, indicating **seniority or better protection**.")

        smallest = df_tranches.loc[df_tranches['Initial Balance ($)'].idxmin()]
        largest = df_tranches.loc[df_tranches['Initial Balance ($)'].idxmax()]
        
        if smallest['Initial Balance ($)'] < largest['Initial Balance ($)'] * 0.2:
            insights.append(f"- Class {smallest['Class']} represents a **small fraction** of the total issuance, which may impact liquidity or investor interest.")

        for insight in insights:
            st.markdown(insight)

        # Optional: Add mock AI risk score
        st.subheader("🧠 AI Risk Simulation")
        df_tranches['Mock Risk Score (1-10)'] = df_tranches['Interest Rate (%)'].apply(lambda x: round((x - 5) * 10, 1))
        st.dataframe(df_tranches[['Class', 'Interest Rate (%)', 'Mock Risk Score (1-10)']])
        

        
    else:
        st.warning("Could not find tranche table in text.")



    
