import streamlit as st
import pymongo
import pandas as pd
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]
collection = db["expenses"]

def display_expenses():
    st.title("All Expenses")

    expenses = list(collection.find())

    if not expenses:
        st.info("No expenses found.")
        return

    for exp in expenses:
        exp["_id"] = str(exp["_id"])
        if exp.get("date") and not isinstance(exp["date"], str):
            exp["date"] = exp["date"].strftime("%Y-%m-%d")

    df = pd.DataFrame(expenses)
    st.dataframe(df, use_container_width=True)

display_expenses()
