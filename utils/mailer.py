from django.core.mail import EmailMessage, send_mail
from django.conf import settings

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def sib_send_mail(html_content, subject, to, sender=None):
    """
    custom mailing function with sendinblues sib_api_v3_sdk
    """
    if sender == None:
        sender = {"email": settings.DEFAULT_FROM_EMAIL,
                  "name": settings.DEFAULT_FROM_NAME}

    configuration = sib_api_v3_sdk.Configuration()

    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content,
        sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: \n {e}")


class Utils:
    """
    Dont use this
    """
    @staticmethod
    def send_mail(data):
        email = EmailMessage(body=data["email_body"],
                             subject=data["email_subject"], to=[data["to"]], from_email=settings.DEFAULT_FROM_EMAIL)
        email.send()

    @staticmethod
    def send_html_mail(data):
        # OLD MAILER
        send_mail(subject=data["email_subject"], message=data["email_stripped_tags"],
                  from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[data["to"]], html_message=data["email_with_tags"])
