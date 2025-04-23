from django.urls import path
from services import views

urlpatterns = [
    path(
        "service-banner/",
        views.PublicServiceBannerView.as_view(),
        name="get-service-banner",
    ),
    path(
        "service-banner/update/",
        views.ProtectedServiceBannerUpdateView.as_view(),
        name="update-service-banner",
    ),
    path("request-service", views.RequestServiceView.as_view(), name="request-service"),
    path(
        "request-services/download",
        views.download_request_services,
        name="download-request-services",
    ),
    path(
        "verify-request",
        views.VerifyServiceRequestEmailView.as_view(),
        name="verify-request",
    ),
    path(
        "newsletter-subscription",
        views.SubscribeToNewsLetterView.as_view(),
        name="newsletter-subscription",
    ),
    path(
        "newsletter-email-verification",
        views.VerifyNewsletterSubscriptionView.as_view(),
        name="newsletter-email-verification",
    ),
    path(
        "newsletter-ui/",
        views.NewsletterUIConfigPublicView.as_view(),
        name="newsletter-ui-public",
    ),
    path(
        "newsletter-ui/update/",
        views.NewsletterUIConfigAdminUpdateView.as_view(),
        name="newsletter-ui-admin-update",
    ),
    path("all-services", views.AllServicesView.as_view(), name="all-services"),
    path(
        "all-services/<int:id>",
        views.AllServicesDetailView.as_view(),
        name="all-services-details",
    ),
    path(
        "all-services/public",
        views.AllServicesViewPublic.as_view(),
        name="all-services-public",
    ),
]
