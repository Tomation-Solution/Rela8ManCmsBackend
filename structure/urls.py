from django.urls import path
from structure import views

urlpatterns = [
    path("sectoral-group", views.SectoralGroupView.as_view(),name="sectoral-group"),
    path("sectoral-group/<int:id>", views.SectoralGroupDetailView.as_view() ,name="sectoral-group-details"),
    path("mrc", views.MRCView.as_view(), name="mrc"),
    path("mrc-service",views.MRCServicesView.as_view(), name="mrc-service"),
    path("mrc-service/<int:id>",views.MRCServicesDetailView.as_view(), name="mrc-service-details"),
    path("mpdcl", views.MPDCLView.as_view(), name="mpdcl"),
    path("mpdcl-service", views.MPDCLServicesView.as_view(), name="mpdcl-service"),
    path("mpdcl-service/<int:id>", views.MPDCLServicesDetialView.as_view(), name="mpdcl-service-details"),

    #public views
    path("sectoral-group/public", views.SectoralGroupPublicView.as_view(),name="sectoral-group-public"),
    path("mrc-service/public", views.MRCServicePublicView.as_view(),name="mrc-service-public"),
    path("mpdcl-service/public", views.MPDCLServicesPublicView.as_view(), name="mpdcl-service-public")
]
