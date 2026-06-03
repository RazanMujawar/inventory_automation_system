from database.db_connection import get_connection

def load_to_sales_table(sales_df):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO sales
    (product_id, quantity_sold, sale_date)
    VALUES (%s, %s, NOW())
    """

    for _, row in sales_df.iterrows():

        product_id = int(row["product_id"])
        quantity_sold = int(row["quantity_sold"])

        cursor.execute(
            query,
            (product_id, quantity_sold)
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("Sales data loaded successfully.")