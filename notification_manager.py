import smtplib
import dotenv

class NotificationManager:
    def __init__(self) -> None:
        self.main_email = "mipysmtp@gmail.com"
        self.mail_password = dotenv.dotenv_values("python.env").get("mail_password")
        self.secondary_email = "mipysmpt@gmail.com"

    def send_notification(self, encoded_msg: bytes) -> None:
        with smtplib.SMTP("smtp.gmail.com", port=587) as main_connection:
                main_connection.starttls()
                main_connection.login(user=self.main_email, password=self.mail_password)
                main_connection.sendmail(from_addr=self.main_email,
                to_addrs=self.secondary_email,
                msg= encoded_msg)