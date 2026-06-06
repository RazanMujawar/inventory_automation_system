import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from modules.email_templates import (
    get_alert_email,
    get_reminder_email,
    get_summary_email,
    get_low_stock_summary_email
)



load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(product_name, stock, reorder_level):

    try:

        sender = "razanmujawar2211@gmail.com"
        receiver = "rizwanamujawar2211@gmail.com"

        body = get_alert_email(product_name, stock, reorder_level)
        msg = MIMEText(body,"html")

        msg["Subject"] = "Inventory Alert"
        msg["From"] = sender
        msg["To"] = receiver

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                sender,
                EMAIL_PASSWORD
            )

            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:

        print("Email Error:", e)


def send_reminder_email():

    sender = "razanmujawar2211@gmail.com"
    receiver = "rizwanamujawar2211@gmail.com"

    body = get_reminder_email()

    msg = MIMEText(
        body,
        "html"
    )

    msg["Subject"] = (
        "Daily Sales Submission Reminder"
    )

    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

    print(
        "Reminder email sent!"
    )

def send_summary_email(
    processing_date,
    processed_file,
    files_processed,
    sales_records,
    low_stock_products
):

    low_stock_count = len(low_stock_products)
    sender = "razanmujawar2211@gmail.com"
    receiver = "rizwanamujawar2211@gmail.com"

    rows = ""

    for product_name, stock, reorder_level in low_stock_products:

        rows += f"""
        <tr>
            <td>{product_name}</td>
            <td>{stock}</td>
            <td>{reorder_level}</td>
        </tr>
        """

    low_stock_html = f"""
    <table border="1"
           cellpadding="10"
           cellspacing="0">

        <tr>
            <th>Product</th>
            <th>Current Stock</th>
            <th>Reorder Level</th>
        </tr>

        {rows}

    </table>
    """

    body = get_summary_email(
    processing_date,
    processed_file,
    files_processed,
    sales_records,
    low_stock_count,
    low_stock_html
    )

    msg = MIMEText(
        body,
        "html"
    )

    msg["Subject"] = (
        "Daily Inventory Processing Report"
    )

    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

    print(
        "Summary email sent!"
    )    

def send_low_stock_summary_email(
    low_stock_products
):

    sender = "razanmujawar2211@gmail.com"
    receiver = "itzrohitpatil08@gmail.com"

    rows = ""

    for _, product_name, stock, reorder_level in low_stock_products:

        rows += f"""
        <tr>
            <td>{product_name}</td>
            <td>{stock}</td>
            <td>{reorder_level}</td>
        </tr>
        """

    low_stock_html = f"""

    <table border="1"
           cellpadding="10"
           cellspacing="0">

        <tr>
            <th>Product</th>
            <th>Current Stock</th>
            <th>Reorder Level</th>
        </tr>

        {rows}

    </table>

    """

    body = get_low_stock_summary_email(
        low_stock_html
    )

    msg = MIMEText(
        body,
        "html"
    )

    msg["Subject"] = (
        "Low Stock Products Alert"
    )

    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

    print(
        "Low stock summary email sent!"
    )
   
if __name__ == "__main__":
    send_email(1, 5)