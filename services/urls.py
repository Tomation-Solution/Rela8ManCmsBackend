from django.urls import path
from services import views

urlpatterns = [
    path("request-service", views.RequestServiceView.as_view(),
         name="request-service"),
    path("verify-request", views.VerifyServiceRequestEmailView.as_view(),
         name="verify-request"),
    path("newsletter-subscription", views.SubscribeToNewsLetterVIew.as_view(),
         name="newsletter-subscription"),
    path("newsletter-email-verification", views.VerifyNewsletterEmailView.as_view(),
         name="newsletter-email-verification"),
    path("all-services", views.AllServicesView.as_view(), name="all-services"),
    path("all-services/<int:id>", views.AllServicesDetailView.as_view(),
         name="all-services-details"),
    path("all-services/public", views.AllServicesViewPublic.as_view(),
         name="all-services-public")
]
