import schedule
import time
from modules.send_email import send_reminder_email

from main import run_pipeline

schedule.every().monday.at(
    "18:00"
).do(send_reminder_email)

schedule.every().tuesday.at(
    "18:00"
).do(send_reminder_email)

schedule.every().wednesday.at(
    "18:00"
).do(send_reminder_email)

schedule.every().thursday.at(
    "18:00"
).do(send_reminder_email)

schedule.every().friday.at(
    "18:00"
).do(send_reminder_email)



while True:

    schedule.run_pending()

    time.sleep(1)