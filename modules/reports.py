import pandas as pd
from database.db_connection import get_connection

def generate_report():

    conn = get_connection()

    query = """
    SELECT *
    FROM products
    """

    df = pd.read_sql(query, conn)

    df.to_csv(
        "reports/inventory_report.csv",
        index=False
    )

    conn.close()