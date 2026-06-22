from database.db_connection import get_connection


def add_product(
    product_name,
    category,
    price,
    stock_quantity,
    reorder_level
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO products
    (
        product_name,
        category,
        price,
        stock_quantity,
        reorder_level
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    cursor.execute(
        query,
        (
            product_name,
            category,
            price,
            stock_quantity,
            reorder_level
        )
    )

    conn.commit()

    new_product_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return new_product_id

def product_exists(product_name):

    product_name = " ".join(
        product_name.strip().split()
    )

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM products
    WHERE LOWER(
        TRIM(product_name)
    ) = LOWER(%s)
    """

    cursor.execute(
        query,
        (product_name,)
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0