import pandas as pd
import streamlit as st

# Load the reference dataset
@st.cache_data
def load_data():
    return pd.read_excel("Trait OverviewMasterv5.xlsx")

df = load_data()

st.title("Trait Feedback Generator")
st.write("Select the desired state for each trait to generate feedback and risk information.")

# Get list of unique traits
traits = df['Name'].unique()

# Dictionary to store user selections
selections = {}

# Create a selection dropdown for each trait
for trait in traits:
    selections[trait] = st.selectbox(f"{trait}", ["Active", "Balanced", "Inactive"], key=trait)

# When user clicks the generate button
if st.button("Generate Output"):
    output_rows = []

    for trait in traits:
        selected_state = selections[trait]
        match = df[(df['Name'] == trait) & (df['State'] == selected_state)]

        if not match.empty:
            feedback = match['Feedback'].values[0]
            risk = match['Risk'].values[0] if not pd.isna(match['Risk'].values[0]) else ""
            output_rows.append({
                "Name": trait,
                "State": selected_state,
                "Feedback": feedback,
                "Risk": risk
            })

    # Create output DataFrame
    output_df = pd.DataFrame(output_rows)

    # Display the output
    st.write("### Generated Output")
    st.dataframe(output_df)

    # Provide download link
    st.download_button(
        label="Download as Excel",
        data=output_df.to_excel(index=False, engine='openpyxl'),
        file_name="Generated_Trait_Feedback.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
