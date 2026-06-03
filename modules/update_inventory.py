from database.db_connection import get_connection
def update_inventory(product_id, quantity):
    connection = get_connection()
    cursor = connection.cursor()
    query = """ UPDATE products
                SET stock_quantity = stock_quantity - %s 
                WHERE product_id = %s"""
    cursor.execute(query, (quantity, product_id))
    connection.commit()
    cursor.close()
    connection.close()
