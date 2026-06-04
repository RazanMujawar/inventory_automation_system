from database.db_connection import get_connection
from modules.send_email import send_email
def generate_alerts():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT product_id, product_name,stock_quantity,reorder_level
    FROM products
    WHERE stock_quantity <= reorder_level
    """

    cursor.execute(query)

    low_stock_products = cursor.fetchall()

    for product_id, product_name, stock, reorder_level in low_stock_products:

    # Check if alert already exists

        cursor.execute(
            """
            SELECT alert_id
            FROM alerts
            WHERE product_id = %s
            AND status = 'OPEN'
            """,
            (product_id,)
        )

        existing_alert = cursor.fetchone()

        # If no open alert exists

        if existing_alert is None:

            insert_query = """
            INSERT INTO alerts
            (
                product_id,
                current_stock,
                alert_date,
                status
            )
            VALUES
            (
                %s,
                %s,
                NOW(),
                'OPEN'
            )
            """

            cursor.execute(
                insert_query,
                (
                    product_id,
                    stock
                )
            )

            send_email(
                product_name,
                stock,
                reorder_level
            )

            print(
                f"Alert created for {product_name}"
            )

        else:

            print(
                f"Open alert already exists for {product_name}"
            ) 
        
        
    conn.commit()

    cursor.close()
    conn.close()