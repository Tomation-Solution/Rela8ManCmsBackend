from django.urls import path
from payments import views

urlpatterns = [
    path("webhook", views.paystack_webhook, name="webhook"),
    path("publications", views.PublicationPaymentView.as_view(),
         name="publication-payment"),
    path("download-publication", views.DownloadPublicationPDF.as_view(),
         name="download-publication"),
    path("view-publication", views.ViewPublicationPDF.as_view(),
         name="view-publication"),
    path("event-training-registration", views.EventTrainingRegistrationView.as_view(),
         name="event-training-registration"),
    path("agm-registration", views.AGMRegistrationView.as_view(),
         name="agm-registration"),
]
