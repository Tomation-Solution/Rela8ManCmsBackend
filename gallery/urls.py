from django.urls import path
from gallery import views

urlpatterns = [
    path("", views.GalleryView.as_view(), name="gallery"),
    path("<int:id>", views.GalleryDetailView.as_view(), name="galleries"),
    path("public", views.GalleryViewPublic.as_view(), name="gallery-public"),
    path("throwback", views.ReturnBack.as_view(), name="throwback"),
]
