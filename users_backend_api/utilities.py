from users_microservice import settings
import smtplib

def sendMessage(email, message):
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(settings.DEV_MAIL, settings.DEV_MAIL_PASS)
    connection.sendmail(settings.DEV_MAIL, email, message)
    connection.quit()
