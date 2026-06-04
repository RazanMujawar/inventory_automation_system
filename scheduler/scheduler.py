import schedule
import time
from modules.send_email import send_reminder_email

schedule.every(1).minutes.do(
    send_reminder_email
)

while True:

    schedule.run_pending()

    time.sleep(1)