from django.urls import path
from events import views

urlpatterns = [
    path("", views.EventView.as_view(), name="event"),
    path(
        "event-banner/",
        views.PublicEventBannerView.as_view(),
        name="get-event-banner",
    ),
    path(
        "event-banner/update/",
        views.ProtectedEventBannerUpdateView.as_view(),
        name="update-event-banner",
    ),
    path("<int:id>", views.EventDetailView.as_view(), name="events"),
    path("public", views.EventViewPublic.as_view(), name="events-public"),
    path("get-agm-event", views.getAGMEvent, name="get-agm-event"),
    path(
        "event-media/",
        views.PublicEventAndMediaContentView.as_view(),
        name="event-media-public",
    ),
    path(
        "event-media/update/",
        views.UpdateEventAndMediaContentView.as_view(),
        name="event-media-update",
    ),
]
