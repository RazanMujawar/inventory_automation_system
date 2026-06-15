import logging

logger = logging.getLogger(__name__)

def update_inventory(
    connection,
    product_id,
    quantity
):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT stock_quantity
        FROM products
        WHERE product_id = %s
        """,
        (product_id,)
    )

    result = cursor.fetchone()

    current_stock = result[0] if result else 0

    new_stock = max(
        0,
        current_stock - quantity
    )

    if quantity > current_stock:

        logger.warning(
            f"Insufficient stock for Product {product_id}"
        )

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

    print(
        f"Product {product_id}: "
        f"{current_stock} -> {new_stock}"
    )

    cursor.close()