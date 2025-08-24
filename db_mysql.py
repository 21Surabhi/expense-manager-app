import mysql.connector
from datetime import datetime

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Surabhi211204",  
        database="db_expenses"
    )

def add_expenses(expenses):
    conn = get_db()
    cursor = conn.cursor()
    query = "INSERT INTO expenses (amount, category, date) VALUES (%s, %s, %s)"
    values = [(exp["amount"], exp["category"], exp["date"]) for exp in expenses]
    cursor.executemany(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount

def edit_expenses(expense_id, updated_data):
    conn = get_db()
    cursor = conn.cursor()
    query = "UPDATE expenses SET amount=%s, category=%s, date=%s WHERE id=%s"
    cursor.execute(query, (
        updated_data.get("amount"),
        updated_data.get("category"),
        updated_data.get("date"),
        expense_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount

def get_expense_by_id(expense_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses WHERE id=%s", (expense_id,))
    expense = cursor.fetchone()
    cursor.close()
    conn.close()
    return expense

def get_all_expenses():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return expenses

def get_all_budgets():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM budgets")
    budgets = cursor.fetchall()
    cursor.close()
    conn.close()
    return budgets

def expenses_less_than_200():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses WHERE amount < 200")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return expenses

def expenses_less_than_1000():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses WHERE amount < 1000")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return expenses

def input_budgets():
    conn = get_db()
    cursor = conn.cursor()
    query = "INSERT INTO budgets (category, budget) VALUES (%s, %s)"
    values = [
        ("Bills", 600),
        ("Entertainment", 700),
        ("Food", 1000),
        ("Health", 1500),
        ("Shopping", 2400),
        ("Transport", 1600)
    ]
    cursor.executemany(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount

def update_budget(category, budget):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM budgets WHERE category = %s", (category,))
    result = cursor.fetchone()
    if result:
        query = "UPDATE budgets SET budget=%s WHERE category=%s"
        cursor.execute(query, (budget, category))
    else:
        query = "INSERT INTO budgets (category, budget) VALUES (%s, %s)"
        cursor.execute(query, (category, budget))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def delete_expense(expense_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Surabhi211204", 
        database="db_expenses"    
    )
    cursor = conn.cursor()

    query = "DELETE FROM expenses WHERE id = %s"
    cursor.execute(query, (expense_id,))

    conn.commit()
    cursor.close()
    conn.close()

