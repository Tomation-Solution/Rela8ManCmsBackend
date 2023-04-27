from django.core.mail import EmailMessage
from django.conf import settings


class Utils:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(body=data["email_body"],
                             subject=data["email_subject"], to=[data["to"]], from_email="popoolakejiah2@gmail.com")
        email.send()
