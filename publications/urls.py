from publications import views
from django.urls import path

urlpatterns = [
    path("", views.PublicationView.as_view(), name="publication"),
    path("<int:id>", views.PublicationDatialView.as_view(), name="publications"),
    path("type", views.PublicationTypeView.as_view(),
         name="publicaton-type"),
    path("type/<int:id>", views.PublicationTypeDetailView.as_view(),
         name="publication-type-detail"),
    path("public", views.PublicationViewPublic.as_view(),
         name="publication-public"),
    path("public/paid-publication",
         views.PublicationViewPaidPublic.as_view(), name="paid_publications"),
]
