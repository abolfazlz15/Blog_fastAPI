import smtplib
from email.message import EmailMessage


class EmailService:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_otp_email(self, recipient_email, otp):
        msg = EmailMessage()
        msg.set_content(f'Your OTP is: {otp}')
        msg['Subject'] = 'OTP for Registration'
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender_email, self.sender_password)

        server.send_message(msg)
        server.quit()
