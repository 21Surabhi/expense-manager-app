import streamlit as st
#from UI_components import load_expenses_into_dataframe, display_expenses_with_edit, display_all_expenses
from db_mongo import get_all_expenses
from UI_components import display_all_expenses

#df = load_expenses_into_dataframe()

#if df.empty:
    #st.info("No expenses found.")
    #st.stop()

#display_expenses_with_edit(df)

expenses = get_all_expenses()

if not expenses:
    st.info("No expenses found.")
    st.stop()

display_all_expenses(expenses)


