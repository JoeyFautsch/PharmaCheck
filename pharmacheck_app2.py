import pandas as pd
import streamlit as st 

df = interactions = pd.read_csv("db_drug_interactionsNEW.csv")
condition_warnings = pd.read_csv("drug_condition_contraindications.csv", encoding="ISO-8859-1")

df = df.rename(columns={
"Interaction Description": "Interaction",
"Drug 1": "Drug_1",
"Drug 2": "Drug_2"
})

def check(drugs):
    warnings = []
    for i in range(len(drugs)):
        for j in range(i+1, len(drugs)):
            d1 = drugs[i].lower()
            d2 = drugs[j].lower()

            match = df[
                ((df['Drug_1'].str.lower() == d1) & (df['Drug_2'].str.lower() == d2)) |
                ((df['Drug_1'].str.lower() == d2) & (df['Drug_2'].str.lower() == d1))
            ]

            for _, row in match.iterrows():
                warnings.append(f"{row['Drug_1']} + {row['Drug_2']}: {row['Interaction']}")
    return warnings

def check_condition_contraindications(drugs, conditions, warning_df):
    flags = []

    for drug in drugs:
        for condition in conditions:
            matches = warning_df[
                (warning_df["Drug Name"].str.lower() == drug.lower()) &
                (warning_df["Condition"].str.lower() == condition.lower())
            ]
            for _, row in matches.iterrows():
                flags.append(
                    f"{row['Drug Name']} + {row['Condition']}: {row['Warning Type']} — {row['Description']}"
                )
    return flags

st.set_page_config(page_title="PharmaCheck", page_icon="💊")
st.title("⚕️ PharmaCheck")
st.write("Check for drug interactions and contraindications with a clean medical interface.")
input_text = st.text_input("Medications, separated by commas")

user_conditions = st.multiselect(
    "Medical History / Medical Conditions",
    [
        "Pregnancy", "Breastfeeding", "Renal insufficiency", "Hepatic impairment", "Diabetes",
        "Cardiovascular disease", "Cardiac arrhythmias", "Seizure history", "GI ulcer history",
        "Asthma", "Hyperkalemia", "History of DVT/PE", "Elderly", "Children", "Smoking",
        "Alcohol use", "Heart failure", "Kidney failure", "Immunosuppression", "Chemotherapy history", "Allergies"
    ]
)
if st.button("Check Interactions"):
    user_drugs = [d.strip() for d in input_text.split(",") if d.strip()]
    results = check(user_drugs)

    if results:
        st.warning("⚠️ Potential Interactions:")
        for r in results:
            st.write(f"• {r}")
    else:
        st.success("✅ No known interactions found.")

# === NEW SECTION: Condition-based warnings ===
    if user_conditions:
        st.subheader("🩺 Condition-Based Warnings")
        condition_results = check_condition_contraindications(user_drugs, user_conditions, condition_warnings)

        if condition_results:
            st.error("⚠️ Drug-condition safety issues detected:")
            for warning in condition_results:
                st.write(f"• {warning}")
        else:
            st.success("✅ No condition-specific warnings found.")