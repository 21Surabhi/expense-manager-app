import streamlit as st
from datetime import datetime
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]
collection = db["expenses"]
CATEGORIES = ["Food", "Transport", "Entertainment", "Health", "Bills", "Shopping", "Other"]

def add_expenses():
    st.title("Expense Entry Form")

    if "expenses" not in st.session_state:
        st.session_state.expenses = []

    idx = len(st.session_state.expenses)

    category = st.selectbox("Choose a category:", CATEGORIES)
    amount = st.number_input("Enter amount:")
    date_str = st.text_input("Enter date (YYYY-MM-DD):")
    description = st.text_input("Enter description (optional):")

    if st.button("Add Expense", key=f"add_btn_{idx}"):
        if date_str and amount:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                amount_value = float(amount)
                expense = {
                    "category": category,
                    "amount": amount_value,
                    "date": date_obj,
                    "description": description
                }
                st.session_state.expenses.append(expense)
                st.success(f"Expense added: {expense}")
            except ValueError:
                st.error("Invalid input. Make sure date is YYYY-MM-DD and amount is a number.")
        else:
            st.error("Date and amount are required.")

    if st.button("Finish Entry", key="finish_entry"):
        if st.session_state.expenses:
            collection.insert_many(st.session_state.expenses)
            st.success(f"{len(st.session_state.expenses)} expenses added successfully!")
            st.session_state.expenses = []
        else:
            st.warning("No expenses to save.")

    if st.button("Go to Edit Expense", key="go_edit"):
        st.session_state.page = "edit_expense"

    if st.button("Display All Expenses", key="display_expenses_btn"):
        st.session_state.page = "display_expenses"

add_expenses()
