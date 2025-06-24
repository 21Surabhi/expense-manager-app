import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]
expenses_col = db["expenses"]
budgets_col = db["budgets"]

st.title("Set Monthly Budget per Category")

all_expenses = list(expenses_col.find())
categories = sorted({e.get("category", "Uncategorized").strip() for e in all_expenses})

if not categories:
    st.info("No expense categories found.")
    st.stop()

existing_budgets = {b["category"]: b["budget"] for b in budgets_col.find()}

updated_budgets = {}

for cat in categories:
    default_val = existing_budgets.get(cat, 0.0)
    budget_input = st.number_input(
        f"Budget for {cat}", min_value=0.0, value=float(default_val), step=100.0
    )
    updated_budgets[cat] = budget_input

if st.button("Save Budgets"):
    try:
        for category, budget in updated_budgets.items():
            budgets_col.update_one(
                {"category": category},
                {"$set": {"budget": budget}},
                upsert=True
            )
        st.success("Budgets saved successfully.")
    except Exception as e:
        st.error(f"Failed to save budgets: {e}")

st.title("Monthly Budget vs Spent per Category")

expenses = list(expenses_col.find())
budgets = {b["category"]: float(b["budget"]) for b in budgets_col.find()}

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
df_grouped["Budget"] = df_grouped["Category"].apply(lambda x: budgets.get(x, 0.0))

months = df_grouped["Month"].drop_duplicates().sort_values()

for month in months:
    label = month.strftime("%B %Y")
    month_data = df_grouped[df_grouped["Month"] == month]

    plot_df = month_data[["Category", "Amount", "Budget"]].melt(
        id_vars="Category", value_vars=["Amount", "Budget"],
        var_name="Type", value_name="Value"
    )

    st.markdown(f"### {label}")
    fig = px.bar(
        plot_df,
        x="Category",
        y="Value",
        color="Type",
        barmode="group",
        text_auto=True,
        title="Budget vs Spent"
    )
    fig.update_layout(xaxis_title="Category", yaxis_title="Amount", legend_title="")
    st.plotly_chart(fig, use_container_width=True, key=label)



st.title("Categories with monthly expense less than 1000")
expenses = list(expenses_col.find())

if not expenses:
    st.info("No expenses found.")
    st.stop()

data = []
for exp in expenses:
    try:
        amount = float(exp.get("amount", 0))
        category = exp.get("category", "Uncategorized").strip()
        date = exp.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        elif not isinstance(date, datetime):
            continue
        month = date.strftime("%Y-%m")  
        data.append((month, category, amount))
    except:
        continue

df = pd.DataFrame(data, columns=["Month", "Category", "Amount"])

grouped = df.groupby(["Month", "Category"], as_index=True).sum()

result = grouped.query("Amount < 1000")

if result.empty:
    st.success("No categories with expenses less than 1000.")
else:
    st.dataframe(result)



st.title("Expenses Less Than 200")

expenses = list(expenses_col.find())

if not expenses:
    st.info("No expenses found.")
    st.stop()

data = []
for exp in expenses:
    try:
        amount = float(exp.get("amount", 0))
        if amount >= 200:
            continue
        category = exp.get("category", "Uncategorized").strip()
        date = exp.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        elif not isinstance(date, datetime):
            continue
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
        })
    except:
        continue

result = pd.DataFrame(data)

if result.empty:
    st.success("No expenses less than 200.")
else:
    st.dataframe(result)
