from database.db_connection import get_connection
import streamlit as st

@st.cache_data(ttl=60)
def get_report_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        """
    )

    total_products = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT SUM(stock_quantity)
        FROM products
        """
    )

    total_stock = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE stock_quantity <= reorder_level
        """
    )

    low_stock = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM alerts
        WHERE status='OPEN'
        """
    )

    open_alerts = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return (
        total_products,
        total_stock,
        low_stock,
        open_alerts
    )