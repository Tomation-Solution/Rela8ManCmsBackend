from django.core.mail import EmailMessage,send_mail
from django.conf import settings


class Utils:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(body=data["email_body"],
                             subject=data["email_subject"], to=[data["to"]], from_email=settings.DEFAULT_FROM_EMAIL)
        email.send()

    @staticmethod
    def send_html_mail(data):
        
        send_mail(subject=data["email_subject"], message=data["email_stripped_tags"], from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[data["to"]], html_message=data["email_with_tags"])
        