from random import randint
from apps.auth.email_service import EmailService


class OTPHandler:
    otp_expiry_minutes = 2

    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def generate_otp(self):
        otp = randint(1000, 9999)
        return str(otp)

    def send(self, email: str):
        otp = self.generate_otp()
        self.email_service.send_otp_email(email, otp)
        return otp
