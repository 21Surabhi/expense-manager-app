import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]
collection = db["expenses"]

st.title("Monthly Expense Analysis")

expenses = list(collection.find())

if not expenses:
    st.info("No expenses found.")
    st.stop()

data = []
for exp in expenses:
    try:
        amount = float(exp.get("amount", 0))
        category = exp.get("category", "Uncategorized")
        date = exp.get("date")
        if isinstance(date, str):
            date = datetime.strptime(date.strip(), "%Y-%m-%d")
        elif not isinstance(date, datetime):
            continue
        normalized_date = datetime(date.year, date.month, 1)
        data.append({
            "Amount": amount,
            "Category": category.strip(),
            "Month": normalized_date.strftime("%B %Y"),
            "SortDate": normalized_date,
            "Year": date.year,
            "MonthNum": date.month
        })
    except:
        continue

df = pd.DataFrame(data)
df.drop_duplicates(subset=["Amount", "Category", "SortDate"], inplace=True)
df.sort_values("SortDate", inplace=True)

unique_months = df[["SortDate", "Month"]].drop_duplicates().sort_values("SortDate")

for i, row in unique_months.iterrows():
    month_dt = row["SortDate"]
    month_label = row["Month"]
    monthly_data = df[df["SortDate"] == month_dt]
    category_summary = monthly_data.groupby("Category", as_index=False)["Amount"].sum()

    st.markdown(f"### {month_label}")
    col1, col2 = st.columns(2)

    with col1:
        bar_fig = px.bar(category_summary, x="Category", y="Amount", title="Bar Chart", text_auto=True)
        bar_fig.update_layout(xaxis_title="Category", yaxis_title="Amount", showlegend=False)
        st.plotly_chart(bar_fig, use_container_width=True, key=f"{month_label}_bar_{i}")

    with col2:
        pie_fig = px.pie(category_summary, names="Category", values="Amount", title="Pie Chart")
        pie_fig.update_traces(textinfo="percent+label")
        st.plotly_chart(pie_fig, use_container_width=True, key=f"{month_label}_pie_{i}")

st.title("Quarterly Expense Analysis")

def get_quarter_number(month):
    return (month - 1) // 3 + 1

df["QuarterNum"] = df["MonthNum"].apply(get_quarter_number)
df["Quarter"] = "Q" + df["QuarterNum"].astype(str)
df["Year_Quarter"] = df["Year"].astype(str) + " " + df["Quarter"]

unique_quarters = df[["Year", "QuarterNum", "Year_Quarter"]].drop_duplicates().sort_values(by=["Year", "QuarterNum"])

for i, row in unique_quarters.iterrows():
    quarter_label = row["Year_Quarter"]
    q_data = df[df["Year_Quarter"] == quarter_label]
    category_summary = q_data.groupby("Category", as_index=False)["Amount"].sum()

    st.markdown(f"### {quarter_label}")
    col1, col2 = st.columns(2)

    with col1:
        bar_fig = px.bar(category_summary, x="Category", y="Amount", title="Bar Chart", text_auto=True)
        bar_fig.update_layout(xaxis_title="Category", yaxis_title="Amount", showlegend=False)
        st.plotly_chart(bar_fig, use_container_width=True, key=f"{quarter_label}_bar_{i}")

    with col2:
        pie_fig = px.pie(category_summary, names="Category", values="Amount", title="Pie Chart")
        pie_fig.update_traces(textinfo="percent+label")
        st.plotly_chart(pie_fig, use_container_width=True, key=f"{quarter_label}_pie_{i}")
