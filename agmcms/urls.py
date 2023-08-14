from django.urls import path
from agmcms import views


urlpatterns = [
    path('homepage', views.AGMHomepageCMSView.as_view(), name='homepage'),
    path("programme", views.AGMProgrammeCMSView.as_view(), name="programme"),
    path("program", views.AGMProgramsView.as_view(), name="program"),
    path("program/<int:id>", views.AGMProgramsDetialedView.as_view(),
         name="program-details"),
    path("speakers", views.AGMSpeakersView.as_view(), name="speakers"),
    path("speakers/<int:id>", views.AGMSpeakersDetialedView.as_view(),
         name="speakers-detailed"),
    path("venue", views.AGMVenueView.as_view(), name="venue"),
    path("exhibition", views.AGMExhibitionCMSView.as_view(), name="exhibition"),
    path("previous-exhibition-images", views.AGMPreviousExhibitionImagesView.as_view(),
         name="previous-exhibition-images"),
    path("previous-exhibition-images/<int:id>", views.AGMPreviousExhibitionImagesDetailedView.as_view(),
         name="previous-exhibition-images-detials"),
    path("faq", views.AGMFAQView.as_view(), name="faq"),
    path("faq/<int:id>", views.AGMFAQDetailView.as_view(), name="faq-details"),

    # PUBLIC URLS
    path("program-public", views.AGMProgramsPublicView.as_view(),
         name="program-public"),
    path("speakers-public", views.AGMSpeakersPublicView.as_view(),
         name="speakers-public"),
    path("previous-exhibition-images-public", views.AGMPreviousExhibitionImagesPublicView.as_view(),
         name="previous-exhibition-images-public"),
    path("faq-public", views.AGMFAQPublicView.as_view(), name="faq-public")
]
