from django.urls import path
from gallery import views

urlpatterns = [
    path("", views.GalleryView.as_view(), name="gallery"),
    path("<int:id>", views.GalleryDetailView.as_view(), name="galleries"),
    path("rename/<int:id>", views.GalleryRenameView.as_view(), name="rename"),
    path("gallery-item/<int:id>",
         views.GalleryItemDetailView.as_view(), name="gallery-item"),
    path("gallery-item/add", views.GalleryAddGalleryItem.as_view(),
         name="add-gallery-item"),
    path("public", views.GalleryViewPublic.as_view(), name="gallery-public"),
]
