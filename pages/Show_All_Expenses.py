import streamlit as st
from UI_components import load_expenses_into_dataframe, display_expenses_with_edit
from db_mongo import 

df = load_expenses_into_dataframe()

if df.empty:
    st.info("No expenses found.")
    st.stop()

display_expenses_with_edit(df)
