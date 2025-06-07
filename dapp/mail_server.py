import smtplib

from .credentials import PASSWORD, SENDER_EMAIL


class MailServer:
    _port = 587  # For starttls
    _smtp_server = "smtp.gmail.com"

    _message = """\
Subject: eVoting System

Your one time password: """

    def send_mail(self, username, receiver_email, OTP):
        #receiver_email = "oloriebiridwan@gmail.com"
        receiver_otp = self._message + OTP

        with smtplib.SMTP(self._smtp_server, self._port) as server:
            server.starttls()
            server.ehlo()
            server.login(SENDER_EMAIL, PASSWORD)
            ask = server.sendmail(SENDER_EMAIL, receiver_email, receiver_otp)
            server.quit()

            return ask


if __name__ == '__main__':
    mail_agent = MailServer()
    print(mail_agent.send_mail(
        'suvambasak22',
        '123456'
    ))
