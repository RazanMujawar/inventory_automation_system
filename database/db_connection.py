import os
import streamlit as st
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool

load_dotenv()

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

host=get_secret("DB_HOST")
port=int(get_secret("DB_PORT"))
user=get_secret("DB_USER")
password=get_secret("DB_PASSWORD")
database=get_secret("DB_NAME")


pool = MySQLConnectionPool(
    pool_name="inventory_pool",
    pool_size=5,
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
def get_connection():
    return pool.get_connection()