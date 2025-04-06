from django.urls import path
from news import views

urlpatterns = [
    path("", views.NewsView.as_view(), name="new"),
    path("<int:id>", views.NewsDetailView.as_view(), name="news"),
    path("public", views.NewsViewPublic.as_view(), name="new-public"),
    path("upload/", views.ImageUploadView.as_view(), name="image-upload"),
]
