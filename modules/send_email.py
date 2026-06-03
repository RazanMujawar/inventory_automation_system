import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(product_id, stock):

    try:

        sender = "razanmujawar2211@gmail.com"
        receiver = "itzrohitpatil08@gmail.com"

        body = f"""
Low Stock Alert

Product ID: {product_id}
Current Stock: {stock}
"""

        msg = MIMEText(body)

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

if __name__ == "__main__":
    send_email(1, 5)