import os
import streamlit as st
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

def get_connection():

    return mysql.connector.connect(
        host=get_secret("DB_HOST"),
        port=int(get_secret("DB_PORT")),
        user=get_secret("DB_USER"),
        password=get_secret("DB_PASSWORD"),
        database=get_secret("DB_NAME")
    )