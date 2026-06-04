import logging
from database.db_connection import get_connection

logger = logging.getLogger(__name__)

def update_inventory(product_id, quantity):

    connection = get_connection()
    cursor = connection.cursor()

    # Get current stock

    cursor.execute(
        """
        SELECT stock_quantity
        FROM products
        WHERE product_id = %s
        """,
        (product_id,)
    )

    result = cursor.fetchone()

    current_stock = result[0]

    # Prevent negative stock

    new_stock = max(
        0,
        current_stock - quantity
    )
    if quantity > current_stock:
        logger.warning(
            f"Insufficient stock for Product {product_id}"
        )
    # Update inventory

    cursor.execute(
        """
        UPDATE products
        SET stock_quantity = %s
        WHERE product_id = %s
        """,
        (
            new_stock,
            product_id
        )
    )

    connection.commit()

    print(
        f"Product {product_id}: "
        f"{current_stock} -> {new_stock}"
    )

    cursor.close()
    connection.close()