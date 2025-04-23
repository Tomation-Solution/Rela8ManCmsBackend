from django.urls import path
from trainings import views

urlpatterns = [
    path("", views.TrainingsView.as_view(), name="training"),
    path(
        "training-banner/",
        views.PublicTrainingBannerView.as_view(),
        name="get-training-banner",
    ),
    path(
        "training-banner/update/",
        views.ProtectedTrainingBannerUpdateView.as_view(),
        name="update-training-banner",
    ),
    path("<int:id>", views.TrainingsDetailView.as_view(), name="trainings"),
    path("public", views.TrainingsViewPublic.as_view(), name="traingings-public"),
]
