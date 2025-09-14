import streamlit as st
from UI_components import display_all_expenses
from db_mongo import get_all_expenses
#from db_mysql import get_all_expenses

expenses = get_all_expenses()

if not expenses:
    st.info("No expenses found.")
    st.stop()

display_all_expenses(expenses)