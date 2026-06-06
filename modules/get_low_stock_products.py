from database.db_connection import get_connection

def get_low_stock_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            product_name,
            stock_quantity,
            reorder_level

        FROM products

        WHERE stock_quantity <= reorder_level
        """
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data