import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd
from db_mongo import edit_expenses  


def show_budget_inputs(categories, existing_budgets):
    updated_budgets = {}
    for cat in categories:
        default_val = existing_budgets.get(cat, 0.0)
        budget_input = st.number_input(
            f"Budget for {cat}", min_value=0.0, value=float(default_val), step=100.0
        )
        updated_budgets[cat] = budget_input
    return updated_budgets

def show_monthly_budget_vs_spent(months, df_grouped):
    for month in months:
        label = month.strftime("%B %Y")
        month_data = df_grouped[df_grouped["Month"] == month]

        if month_data.empty:
            continue

        plot_df = month_data[["Category", "Amount", "Budget"]].melt(
            id_vars="Category", value_vars=["Amount", "Budget"],
            var_name="Type", value_name="Value"
        )

        st.markdown(f"### {label}")
        fig = px.bar(
            plot_df, x="Category", y="Value", color="Type",
            barmode="group", text_auto=True, title="Budget vs Spent"
        )
        fig.update_layout(xaxis_title="Category", yaxis_title="Amount", legend_title="")
        st.plotly_chart(fig, use_container_width=True, key=label)


def display_monthly_expenses(unique_months, df):
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

def display_quarterly_expenses(unique_quarters, df):
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


def display_all_expenses(expenses):
    st.title("All Expenses")

    if not expenses:
        st.info("No expenses found.")
        return

    headers = ["Category", "Amount", "Date", "Description", "Actions"]
    cols = st.columns([2, 2, 2, 3, 1])
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    for i, exp in enumerate(expenses):
        exp_id = str(exp["_id"])
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])

        col1.write(exp.get("category", ""))
        col2.write(f"₹{exp.get('amount', 0)}")
        date_str = exp["date"].strftime("%Y-%m-%d") if isinstance(exp["date"], datetime) else str(exp["date"])
        col3.write(date_str)
        col4.write(exp.get("description", ""))

        if col5.button("Edit", key=f"edit_{i}"):
            st.session_state.selected_expense_id = exp_id
            st.switch_page("pages/Edit_Expenses.py")


def edit_expense_form(exp, categories, exp_id):
    st.title("Edit Expense")

    if "Other" not in categories:
        categories.append("Other")

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
        if not final_category:
            st.error("Category cannot be empty.")
        else:
            try:
                updated_data = {
                    "category": final_category,
                    "amount": new_amount,
                    "date": datetime.combine(new_date, datetime.min.time()),
                    "description": new_desc
                }
                edit_expenses(exp_id, updated_data)
                st.success("Expense updated successfully.")
                del st.session_state.selected_expense_id
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Update failed: {e}")


CATEGORIES = ["Food", "Transport", "Entertainment", "Health", "Bills", "Shopping", "Other"]

def expense_entry_form():
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
                expense = {
                    "category": category,
                    "amount": float(amount),
                    "date": date_obj,
                    "description": description
                }
                st.session_state.expenses.append(expense)
                st.success(f"Expense added: {expense}")
            except ValueError:
                st.error("Invalid input. Use YYYY-MM-DD for date and a valid number for amount.")
        else:
            st.error("Date and amount are required.")

def finish_entry_button(add_expenses_fn):
    if st.button("Finish Entry"):
        if st.session_state.expenses:
            add_expenses_fn(st.session_state.expenses)
            st.success(f"{len(st.session_state.expenses)} expenses added successfully!")
            st.session_state.expenses = []
        else:
            st.warning("No expenses to save.")

def navigation_buttons():
    if st.button("Go to Edit Expense"):
        st.switch_page("pages/Edit_Expense.py")

def show_expenses_less_than_200(result_df):
    if result_df.empty:
        st.success("No expenses less than 200.")
    else:
        st.markdown("### Expenses Less Than 200")
        st.dataframe(result_df)

def show_expenses_less_than_1000(result_df):
    st.markdown("### Categories with Monthly Expense Less Than 1000")
    
    if result_df.empty:
        st.success("No categories with expenses less than 1000.")
    else:
        st.dataframe(result_df)



"""
import streamlit as st
import pandas as pd
from datetime import datetime
from db_mysql import edit_expenses, get_all_expenses, delete_expense

def load_expenses_into_dataframe():
    expenses = get_all_expenses()
    df = pd.DataFrame(expenses)
    if not df.empty:
        df.rename(columns={
            "id": "ID",
            "category": "Category",
            "amount": "Amount",
            "date": "Date",
            "description": "Description"
        }, inplace=True)
    return df



def display_all_expenses(expenses):
    if not expenses:
        st.write("No expenses to display.")
        return
    
    st.subheader("All Expenses")
    for expense in expenses:
        st.write(f"Category: {expense['category']}, Amount: {expense['amount']}, Date: {expense['date']}")



def display_expenses_with_edit(df):
    if df.empty:
        st.write("No expenses to display.")
        return
    
    st.subheader("All Expenses")
    
    headers = ["Category", "Amount", "Date", "Description", "Actions"]
    cols = st.columns([2, 2, 2, 3, 1])
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    print ("dataframe",df)
    for i, exp in df.iterrows():
        exp_id = exp["ID"]  
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])

        col1.write(exp["Category"])
        col2.write(f"₹{exp['Amount']}")
        date_str = exp["Date"].strftime("%Y-%m-%d") if isinstance(exp["Date"], datetime) else str(exp["Date"])
        col3.write(date_str)
        col4.write(exp["Description"] if "Description" in exp else "")

        if col5.button("Edit", key=f"edit_{i}"):
            st.session_state.selected_expense_id = exp_id
            st.switch_page("pages/Edit_Expenses.py")

        if col6.button("Delete", key=f"delete_{i}"):
            delete_expense(exp_id)
            st.success("Expense deleted successfully!")
            st.rerun()

def display_expenses_table(expenses):
    if not expenses:
        st.write("No expenses to display.")
        return
    
    df = pd.DataFrame(expenses)
    df.rename(columns={
        "id": "ID",
        "category": "Category",
        "amount": "Amount",
        "date": "Date",
        "description": "Description"
    }, inplace=True)

    st.subheader("All Expenses")
    st.dataframe(df, use_container_width=True)
"""

    