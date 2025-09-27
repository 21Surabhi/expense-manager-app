import pymongo
from bson import ObjectId
from datetime import datetime

def get_db():
    client = pymongo.MongoClient("mongodb+srv://surabhihegde21:GRixrjhlFMBMRexT@cluster0.rl4aqdh.mongodb.net/")
    return client["expense_manager"]

def add_expenses(expenses):
    db = get_db()
    return db["expenses"].insert_many(expenses)

def edit_expenses(expense_id, updated_data):
    db = get_db()
    return db["expenses"].update_one(
        {"_id": ObjectId(expense_id)},
        {"$set": updated_data}
    )

def get_expense_by_id(expense_id):
    db = get_db()
    return db["expenses"].find_one({"_id": ObjectId(expense_id)})

def get_all_expenses():
    db = get_db()
    return list(db["expenses"].find())

def get_all_budgets():
    db = get_db()
    return list(db["budgets"].find())

def expenses_less_than_200():
    db = get_db()
    return list(db["expenses"].find({"amount": {"$lt": 200}}))

def expenses_less_than_1000():
    db = get_db()
    return list(db["expenses"].find({"amount": {"$lt": 1000}}))

def input_budgets():
    db = get_db()
    return db["budgets"].insert_many([
        {"category": "Bills", "budget": 600}, 
        {"category": "Entertainment", "budget": 700}, 
        {"category": "Food", "budget": 1000}, 
        {"category": "Health", "budget": 1500}, 
        {"category": "Shopping", "budget": 2400},
        {"category": "Transport", "budget": 1600}
    ])

def update_budget(category, new_budget):
    db = get_db()
    result = db["budgets"].update_one(
        {"category": category},
        {"$set": {"budget": new_budget}}
    )
    return result.modified_count





