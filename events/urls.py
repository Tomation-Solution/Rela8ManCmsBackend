from django.urls import path
from events import views

urlpatterns = [
    path("", views.EventView.as_view(), name="event"),
    path("<int:id>", views.EventDetailView.as_view(), name="events"),
    path("public", views.EventViewPublic.as_view(), name="events-public"),
]
