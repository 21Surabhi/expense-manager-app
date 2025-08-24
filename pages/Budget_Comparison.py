import streamlit as st
import pandas as pd
from datetime import datetime
from db_mysql import (
    get_all_expenses,
    get_all_budgets,
    update_budget,
    expenses_less_than_1000,
    expenses_less_than_200
)
from UI_components import (
    show_budget_inputs,
    show_monthly_budget_vs_spent,
    show_expenses_less_than_1000,
    show_expenses_less_than_200
)

st.title("Set Monthly Budget per Category")


expenses = get_all_expenses()
budgets_list = get_all_budgets()
categories = sorted({e.get("category", "Uncategorized").strip() for e in expenses})

if not categories:
    st.info("No expense categories found.")
    st.stop()


existing_budgets = {b["category"]: b["budget"] for b in budgets_list}
updated_budgets = show_budget_inputs(categories, existing_budgets)


if st.button("Save Budgets"):
    try:
        for category, budget in updated_budgets.items():
            update_budget(category, budget)  
        st.success("Budgets saved successfully.")
    except Exception as e:
        st.error(f"Failed to save budgets: {e}")


st.title("Monthly Budget vs Spent per Category")

if not expenses:
    st.info("No expense data found.")
    st.stop()

data = []
for exp in expenses:
    try:
        amount = float(exp.get("amount", 0))
        category = exp.get("category", "Uncategorized").strip()
        date = exp.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date.strip(), "%Y-%m-%d")
        elif not isinstance(date, datetime):
            continue
        month = datetime(date.year, date.month, 1)
        data.append({
            "Amount": amount,
            "Category": category,
            "Month": month
        })
    except:
        continue

df = pd.DataFrame(data)
df_grouped = df.groupby(["Month", "Category"], as_index=False)["Amount"].sum()
df_grouped["MonthLabel"] = df_grouped["Month"].dt.strftime("%B %Y")
df_grouped["Budget"] = df_grouped["Category"].apply(lambda x: existing_budgets.get(x, 0.0))

months = df_grouped["Month"].drop_duplicates().sort_values()
show_monthly_budget_vs_spent(months, df_grouped)


expenses_1000 = expenses_less_than_1000()

cleaned = []
for exp in expenses_1000:
    try:
        amount = float(exp.get("amount", 0))
        category = exp.get("category", "Uncategorized").strip()
        date = exp.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date.strip(), "%Y-%m-%d")
        elif not isinstance(date, datetime):
            continue
        cleaned.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
        })
    except:
        continue

df_1000 = pd.DataFrame(cleaned)
if df_1000.empty:
    st.info("No expenses under 1000 found.")
else:
    show_expenses_less_than_1000(df_1000)


expenses_200 = expenses_less_than_200()

small_expenses = []
for exp in expenses_200:
    try:
        amount = float(exp.get("amount", 0)) 
        category = exp.get("category", "Uncategorized").strip()
        date = exp.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date.strip(), "%Y-%m-%d")
        elif not isinstance(date, datetime):
            continue
        small_expenses.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
        })
    except:
        continue

df_200 = pd.DataFrame(small_expenses)
if not df_200.empty:
    show_expenses_less_than_200(df_200)
else:
    st.info("No expenses under 200 found.")