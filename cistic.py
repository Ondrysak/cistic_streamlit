import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Trello Defect Cleaner", layout="wide")
st.title("🛠️ Trello Defect CSV Cleaner")

uploaded_file = st.file_uploader("📤 Nahraj Trello CSV export", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Filter for relevant lists
        filtered = df[df["List Name"].isin(["Defekty - Milestone 4", "Reopen defekty - Milestone 4"])].copy()

        # Clean up label text
        filtered["Labels"] = filtered["Labels"].apply(lambda x: re.sub(r"\s*\(.*?\)", "", str(x)).strip())

        # Convert date and sort
        filtered["Last Activity Date"] = pd.to_datetime(filtered["Last Activity Date"])
        filtered = filtered.sort_values(by=["Labels", "Last Activity Date"])

        # Select desired columns
        result = filtered[["Labels", "Card Name", "Card URL", "List Name"]].reset_index(drop=True)

        # Show preview
        st.subheader("🔍 Náhled vyčištěných dat")
        st.dataframe(result, use_container_width=True)

        # Prepare download
        csv = result.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Stáhnout vyčištěný CSV", data=csv, file_name="filtered_defects.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Chyba při zpracování souboru: {e}")
else:
    st.info("Nahraj CSV export z Trella pro zpracování.")
