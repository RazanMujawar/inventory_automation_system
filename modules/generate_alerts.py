from database.db_connection import get_connection
from modules.send_email import send_email
from modules.send_email import send_low_stock_summary_email

def generate_alerts():
    
    new_alert_products = []

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

        existing_alert = cursor.fetchall()

        # If no open alert exists

        new_alert_products.append(
    (
        product_id,
        product_name,
        stock,
        reorder_level
    )
)
        
        
        if len(existing_alert) == 0:

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

            print(
                f"Alert created for {product_name}"
            )

        else:

            print(
                f"Open alert already exists for {product_name}"
            ) 
    
    
    if len(new_alert_products) > 0:

        send_low_stock_summary_email(
        new_alert_products
    )
        
    conn.commit()

    cursor.close()
    conn.close()