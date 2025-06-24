import streamlit as st
import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]
collection = db["expenses"]

st.title("All Expenses")

expenses = list(collection.find())

if not expenses:
    st.info("No expenses found.")
    st.stop()

headers = ["Category", "Amount", "Date", "Description", "Actions"]
cols = st.columns([2, 2, 2, 3, 1])
for col, header in zip(cols, headers):
    col.markdown(f"**{header}**")

for i, exp in enumerate(expenses):
    exp_id = str(exp["_id"])
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])

    col1.write(exp["category"])
    col2.write(f"₹{exp['amount']}")
    date_str = exp["date"].strftime("%Y-%m-%d") if isinstance(exp["date"], datetime) else exp["date"]
    col3.write(date_str)
    col4.write(exp.get("description", ""))

    if col5.button("Edit", key=f"edit_{i}"):
        st.session_state.selected_expense_id = exp_id
        st.switch_page("pages/Edit_Expenses.py")  