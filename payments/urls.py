from django.urls import path
from payments import views
from payments.specific_views import views as specifics
from payments.specific_views import flutterwave_views

urlpatterns = [
    # WEBHOOKS
    path("webhook", views.paystack_webhook, name="webhook"),
    path("flutterwave-webhook", flutterwave_views.flutterwave_webhook,
         name="flutterwave-webhook"),  # https://web-production-9688.up.railway.app/api/payments/flutterwave-webhook

    #     https://web-production-9688.up.railway.app/api/payments/flutterwave-webhook
    # WEBHOOKS

    path("test-flutterwave-payments", flutterwave_views.TestFlutterWavePayment.as_view(),
         name="test-flutterwave-payments"),

    path("publications", views.PublicationPaymentView.as_view(),
         name="publication-payment"),
    path("download-publication", views.DownloadPublicationPDF.as_view(),
         name="download-publication"),
    path("view-publication", views.ViewPublicationPDF.as_view(),
         name="view-publication"),
    path("event-training-registration", views.EventTrainingRegistrationView.as_view(),
         name="event-training-registration"),

    # AGM URLS
    path("luncheon/<int:id>", specifics.LuncheonViews.as_view(), name="luncheon"),
    path("exhibition-boot", specifics.ExhibitionBootView.as_view(),
         name="exhibition-boot"),
    path("exhibition-boot/<int:id>", specifics.ExhibitionBootDetailView.as_view(),
         name="exhibition-boot-details"),
    path("member-agm-registration", specifics.MembersAGMRegistrationView.as_view(),
         name="member-agm-registration"),
    path("exhibitor-agm-registration", specifics.ExhibitorsAGMRegistrationView.as_view(),
         name="exhibitor-agm-registration"),
    path("others-agm-registration", specifics.OthersAGMRegistrationView.as_view(),
         name="others-agm-registration"),
    path("agm-invitation", specifics.AGMInvitationView.as_view(),
         name="agm-invitation"),
    path("agm-invitation-verification", specifics.AGMInvitationVerification.as_view(),
         name="agm-invitation-verification"),
    path("quick-agm-registration", specifics.QuickRegistrationView.as_view(),
         name="quick-agm-registration"),

    # PUBLIC URLS
    path("exhibition-boot/public", specifics.ExhibitionBootPublicView.as_view(),
         name="exhibition-boot-public"),
    path("luncheon/public", specifics.LuncheonPublicView.as_view(),
         name="luncheon-public"),
]
