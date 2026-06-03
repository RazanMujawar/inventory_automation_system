from database.db_connection import get_connection
from modules.send_email import send_email
def generate_alerts():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT product_id, stock_quantity
    FROM products
    WHERE stock_quantity <= reorder_level
    """

    cursor.execute(query)

    low_stock_products = cursor.fetchall()

    for product_id, stock in low_stock_products:

        insert_query = """
        INSERT INTO alerts
        (product_id, current_stock, alert_date, status)
        VALUES (%s, %s, NOW(), 'OPEN')
        """

        cursor.execute(
            insert_query,
            (product_id, stock)
        )
        send_email(product_id, stock) 
        
        
    conn.commit()

    cursor.close()
    conn.close()