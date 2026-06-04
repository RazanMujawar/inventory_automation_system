import pandas as pd
from database.db_connection import get_connection

def generate_reports():

    conn = get_connection()

    # ----------------------------------
    # Inventory Report
    # ----------------------------------

    inventory_query = """
    SELECT
        product_name,
        stock_quantity,
        reorder_level
    FROM products
    """

    inventory_df = pd.read_sql(
        inventory_query,
        conn
    )

    inventory_df.to_csv(
        "reports/inventory_report.csv",
        index=False
    )

    # ----------------------------------
    # Sales Summary Report
    # ----------------------------------

    sales_query = """
    SELECT
        p.product_name,
        SUM(s.quantity_sold) AS total_sold

    FROM sales s

    JOIN products p
    ON s.product_id = p.product_id

    GROUP BY p.product_name
    """

    sales_df = pd.read_sql(
        sales_query,
        conn
    )

    sales_df.to_csv(
        "reports/sales_summary.csv",
        index=False
    )

    # ----------------------------------
    # Low Stock Report
    # ----------------------------------

    low_stock_query = """
    SELECT
        product_name,
        stock_quantity

    FROM products

    WHERE stock_quantity <= reorder_level
    """

    low_stock_df = pd.read_sql(
        low_stock_query,
        conn
    )

    low_stock_df.to_csv(
        "reports/low_stock_report.csv",
        index=False
    )

    conn.close()

    print("Reports generated successfully!")