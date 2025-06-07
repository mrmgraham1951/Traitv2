import streamlit as st
import pandas as pd
from io import BytesIO

@st.cache_data
def load_data():
    return pd.read_excel("Trait OverviewMasterv5.xlsx", engine="openpyxl")

def generate_feedback(df, selections):
    rows = []
    for i, row in df.iterrows():
        state = selections.get(row["Name"])
        feedback = row[state.capitalize()]
        risk = row["Risk"]
        rows.append({"Trait": row["Name"], "State": state.capitalize(), "Feedback": feedback, "Risk": risk})
    return pd.DataFrame(rows)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

df = load_data()

st.title("Trait Feedback Generator")

st.markdown("Select a state (Active, Balanced, Inactive) for each trait.")

selections = {}
for trait in df["Name"].unique():
    selections[trait] = st.selectbox(f"{trait}", ["Active", "Balanced", "Inactive"], key=trait)

if st.button("Generate Feedback"):
    output_df = generate_feedback(df, selections)
    st.dataframe(output_df)

    excel_data = to_excel(output_df)
    st.download_button(
        label="Download Feedback as Excel",
        data=excel_data,
        file_name="trait_feedback_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

