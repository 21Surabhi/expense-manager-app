import streamlit as st
import pymongo
from datetime import datetime
from bson import ObjectId

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]
collection = db["expenses"]

exp_id = st.session_state.get("selected_expense_id")

if not exp_id:
    st.warning("No expense selected for editing.")
    st.stop()

exp = collection.find_one({"_id": ObjectId(exp_id)})

if not exp:
    st.error("Expense not found.")
    st.stop()

all_expenses = list(collection.find())
categories = sorted({e["category"] for e in all_expenses if "category" in e})

if "Other" not in categories:
    categories.append("Other")

st.title("Edit Expense")

default_index = categories.index(exp["category"]) if exp["category"] in categories else categories.index("Other")
selected_category = st.selectbox("Category", options=categories, index=default_index)

if selected_category == "Other":
    custom_category = st.text_input("Enter new category").strip()
    final_category = custom_category if custom_category else None
else:
    final_category = selected_category

new_amount = st.number_input("Amount", min_value=0.0, value=float(exp["amount"]), format="%.2f")

date_str = exp["date"].strftime("%Y-%m-%d") if isinstance(exp["date"], datetime) else str(exp["date"])
new_date = st.date_input("Date", value=datetime.strptime(date_str, "%Y-%m-%d"))

new_desc = st.text_input("Description", value=exp.get("description", ""))

if st.button("Save"):
    try:
        if not final_category:
            st.error("Category cannot be empty.")
        else:
            collection.update_one(
                {"_id": ObjectId(exp_id)},
                {
                    "$set": {
                        "category": final_category,
                        "amount": new_amount,
                        "date": datetime.combine(new_date, datetime.min.time()),
                        "description": new_desc,
                    }
                },
            )
            st.success("Expense updated successfully.")
            del st.session_state.selected_expense_id
    except Exception as e:
        st.error(f"Update failed: {e}")

if st.button("Back"):
    del st.session_state.selected_expense_id
    st.switch_page("pages/Display_Expenses.py")
