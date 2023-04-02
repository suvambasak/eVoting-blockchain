import smtplib
import string
import random

port = 587  # For starttls
smtp_server = "smtp.gmail.com"

sender_email = "username@email.com"
password = "passwd123"


def generate_opt(length):
    otp = ''
    for _ in range(length):
        otp += random.choice(string.digits)
    return otp


def send_mail(receiver_email, OTP):
    message = """\
Subject: eVoting System

Your one time password: """

    message += OTP

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()


send_mail(
    "suvambasak22@iitk.ac.in",
    generate_opt(6)
)
