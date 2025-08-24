import streamlit as st
from db_mongo import add_expenses
#from db_mysql import add_expenses
from UI_components import expense_entry_form, finish_entry_button, navigation_buttons

st.title("Expense Entry Form")

expense_entry_form()
finish_entry_button(add_expenses)  
navigation_buttons()
