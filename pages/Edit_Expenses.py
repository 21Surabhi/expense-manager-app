import streamlit as st
from db_mongo import get_expense_by_id, get_all_expenses  
#from db_mysql import get_expense_by_id, get_all_expenses
from UI_components import edit_expense_form

exp_id = st.session_state.get("selected_expense_id")

if not exp_id:
    st.warning("No expense selected for editing.")
    st.stop()

exp = get_expense_by_id(exp_id)
if not exp:
    st.error("Expense not found.")
    st.stop()

all_expenses = get_all_expenses()
categories = sorted({e["category"] for e in all_expenses if "category" in e})

edit_expense_form(exp, categories, exp_id)

if st.button("Back"):
    del st.session_state["selected_expense_id"]
    st.switch_page("pages/Display_Expenses.py")
