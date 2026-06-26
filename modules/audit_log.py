from database.db_connection import get_connection


def add_audit_log(action_type, description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (
            action_type,
            description
        )
        VALUES (%s, %s)
    """, (action_type, description))

    conn.commit()

    cursor.close()
    conn.close()


def get_audit_logs():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY created_at DESC
    """)

    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return logs