from database.db_connection import get_connection


def add_category(category_name):

    category_name = " ".join(
        category_name.strip().split()
    )

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO categories
    (
        category_name
    )
    VALUES
    (
        %s
    )
    """

    cursor.execute(
        query,
        (category_name,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def category_exists(category_name):

    category_name = " ".join(
        category_name.strip().split()
    )

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM categories
    WHERE LOWER(category_name)
    =
    LOWER(%s)
    """

    cursor.execute(
        query,
        (category_name,)
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0


def get_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT category_name
        FROM categories
        ORDER BY category_name
        """
    )

    categories = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return categories