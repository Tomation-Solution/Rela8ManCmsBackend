from django.urls import path
from trainings import views

urlpatterns = [
    path("", views.TrainingsView.as_view(), name="training"),
    path("<int:id>", views.TrainingsDetailView.as_view(), name="trainings"),
    path("public", views.TrainingsViewPublic.as_view(), name="traingings-public"),
]
