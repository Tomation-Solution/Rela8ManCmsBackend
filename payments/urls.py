# payments/urls.py

from django.urls import path
from .views import (
    PaymentRedirectView,
    PublicationPaymentListView,
    EventTrainingRegistrationListView,
    publication_payment_download,
    event_training_registration_download,
    DownloadPublicationPDFView,
)
from payments.specific_views import views as specifics

urlpatterns = [
    path("initialize/", PaymentRedirectView.as_view(), name="initialize_payment"),
    path(
        "publication/download/<uuid:token>/",
        DownloadPublicationPDFView.as_view(),
        name="download_publication",
    ),
    # Paginated API views with filters
    path(
        "publication-payments/",
        PublicationPaymentListView.as_view(),
        name="publication-payment-list",
    ),
    path(
        "event-training-registrations/",
        EventTrainingRegistrationListView.as_view(),
        name="event-training-registration-list",
    ),
    # PDF download views
    path(
        "publication-payments/download/",
        publication_payment_download,
        name="publication-payment-download",
    ),
    path(
        "event-training-registrations/download/",
        event_training_registration_download,
        name="event-training-registration-download",
    ),
    # AGM URLS
    path("luncheon/<int:id>", specifics.LuncheonViews.as_view(), name="luncheon"),
    path(
        "exhibition-boot",
        specifics.ExhibitionBootView.as_view(),
        name="exhibition-boot",
    ),
    path(
        "exhibition-boot/<int:id>",
        specifics.ExhibitionBootDetailView.as_view(),
        name="exhibition-boot-details",
    ),
    path(
        "member-agm-registration",
        specifics.MembersAGMRegistrationView.as_view(),
        name="member-agm-registration",
    ),
    path(
        "exhibitor-agm-registration",
        specifics.ExhibitorsAGMRegistrationView.as_view(),
        name="exhibitor-agm-registration",
    ),
    path(
        "others-agm-registration",
        specifics.OthersAGMRegistrationView.as_view(),
        name="others-agm-registration",
    ),
    path(
        "agm-invitation", specifics.AGMInvitationView.as_view(), name="agm-invitation"
    ),
    path(
        "agm-invitation-verification",
        specifics.AGMInvitationVerification.as_view(),
        name="agm-invitation-verification",
    ),
    path(
        "quick-agm-registration",
        specifics.QuickRegistrationView.as_view(),
        name="quick-agm-registration",
    ),
    # PUBLIC URLS
    path(
        "exhibition-boot/public",
        specifics.ExhibitionBootPublicView.as_view(),
        name="exhibition-boot-public",
    ),
    path(
        "luncheon/public",
        specifics.LuncheonPublicView.as_view(),
        name="luncheon-public",
    ),
]
