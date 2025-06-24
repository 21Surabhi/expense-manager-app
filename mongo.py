import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["expense_manager"]