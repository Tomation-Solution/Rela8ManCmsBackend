from django.core.mail import EmailMessage, send_mail
from django.conf import settings

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


# def sib_send_mail(html_content, subject, to, sender=None):
#     """
#     Custom mailing function with SendinBlue's sib_api_v3_sdk
#     """
#     if sender is None:
#         sender = {
#             "email": settings.DEFAULT_FROM_EMAIL,
#             "name": settings.DEFAULT_FROM_NAME,
#         }

#     configuration = sib_api_v3_sdk.Configuration()
#     configuration.api_key["api-key"] = settings.SENDINBLUE_API_KEY
#     api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
#         sib_api_v3_sdk.ApiClient(configuration)
#     )
#     send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
#         to=to, html_content=html_content, sender=sender, subject=subject
#     )

#     try:
#         # Attempt to send using SendinBlue
#         api_response = api_instance.send_transac_email(send_smtp_email)
#         print(api_response)
#     except ApiException as e:
#         # If an exception occurs, fallback to Django's default mailer
#         print(f"Exception when sending email via SendinBlue: {e}")
#         print("Falling back to Django's default mailer...")

#         # Prepare and send the email using Django's default mailer
#         try:
#             # email = EmailMessage(
#             #     body="",
#             #     html_message=html_content,
#             #     subject=subject,
#             #     to=[recipient["email"] for recipient in to],
#             #     from_email=sender,
#             # )
#             # email.send()

#             send_mail(
#                 subject=subject,
#                 message="",
#                 from_email=sender,
#                 recipient_list=[recipient["email"] for recipient in to],
#                 html_message=html_content,
#             )
#             print("Email sent successfully using Django's default mailer.")
#         except Exception as e:
#             print(f"Exception when sending email via Django's default mailer: {e}")


from django.core.mail import send_mail
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def sib_send_mail(html_content, subject, to, sender=None, cc=None):
    """
    Custom mailing function with SendinBlue's sib_api_v3_sdk
    """

    sender = {
        "email": settings.DEFAULT_FROM_EMAIL,
        "name": settings.DEFAULT_FROM_NAME,
    }

    print(settings.SENDINBLUE_API_KEY)
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        cc=cc,  # Add cc here
        html_content=html_content,
        sender=sender,
        subject=subject,
    )

    try:
        # Attempt to send using SendinBlue
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        # If an exception occurs, fallback to Django's default mailer
        print(f"Exception when sending email via SendinBlue: {e}")
        print("Falling back to Django's default mailer...")

        # Prepare and send the email using Django's default mailer
        try:
            send_mail(
                subject=subject,
                message="",
                from_email=sender["email"],
                recipient_list=([recipient["email"] for recipient in to]),
                html_message=html_content,
                # cc=[recipient["email"] for recipient in cc] if cc else [],
            )
            print("Email sent successfully using Django's default mailer.")
        except Exception as e:
            print(f"Exception when sending email via Django's default mailer: {e}")


class Utils:
    """
    Dont use this
    """

    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            body=data["email_body"],
            subject=data["email_subject"],
            to=[data["to"]],
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        email.send()

    @staticmethod
    def send_html_mail(data):
        # OLD MAILER
        send_mail(
            subject=data["email_subject"],
            message=data["email_stripped_tags"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data["to"]],
            html_message=data["email_with_tags"],
        )
