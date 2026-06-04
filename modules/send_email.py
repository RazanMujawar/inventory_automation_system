import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from modules.email_templates import get_alert_email


load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(product_name, stock, reorder_level):

    try:

        sender = "razanmujawar2211@gmail.com"
        receiver = "itzrohitpatil08@gmail.com"

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
    receiver = "itzrohitpatil08@gmail.com"

    body = """
    <h2>📊 Daily Sales Data Reminder</h2>

    <p>
    Please upload today's sales file before 9:00 PM
    for inventory processing.
    </p>

    <p>
    Expected Format:
    sales_YYYYMMDD.csv
    </p>
    """

    msg = MIMEText(body, "html")

    msg["Subject"] = "Daily Sales Reminder"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(sender, EMAIL_PASSWORD)

        server.send_message(msg)

    print("Reminder email sent!")
    
    
if __name__ == "__main__":
    send_email(1, 5)