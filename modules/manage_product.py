from database.db_connection import get_connection


def get_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name
        FROM products
        ORDER BY product_name
    """)

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return products


def get_product_details(product_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM products
        WHERE product_id = %s
    """, (product_id,))

    product = cursor.fetchone()

    cursor.close()
    conn.close()

    return product


def update_product(
    product_id,
    product_name,
    category,
    price,
    reorder_level,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET
            product_name=%s,
            category=%s,
            price=%s,
            reorder_level=%s,
            status=%s
        WHERE product_id=%s
    """,
    (
        product_name,
        category,
        price,
        reorder_level,
        status,
        product_id
    ))

    conn.commit()

    cursor.close()
    conn.close()
    
def product_exists_except_current(
    product_name,
    product_id
):

    product_name = " ".join(
        product_name.strip().split()
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE
            LOWER(TRIM(product_name))
            =
            LOWER(%s)
        AND
            product_id <> %s
    """,
    (
        product_name,
        product_id
    ))

    exists = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return exists > 0