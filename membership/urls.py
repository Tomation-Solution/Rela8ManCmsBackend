from django.urls import path
from membership import views

urlpatterns = [
    path("why-join", views.WhyJoinManView.as_view(), name="why-join"),
    path("why-join/<int:id>", views.WhyJoinManDetailView.as_view(),
         name="why-join-details"),
    path("join-step", views.JoiningStepView.as_view(), name="join-step"),
    path("join-step/<int:id>", views.JoiningStepDetailView.as_view(),
         name="join-step-details"),
    path("faq", views.FAQsView.as_view(), name="faq"),
    path("faq/<int:id>", views.FAQsDetailView.as_view(), name="faq-details"),
    path("home-main/", views.HomePageView.as_view(), name="home-main"),
    path("why-we-are-unique/", views.WhyWeAreUniqueView.as_view(),
         name="why-we-are-unique"),
    path("why-we-are-unique/<int:id>", views.WhyWeAreUniqueDetailView.as_view(),
         name="why-we-are-unique-details"),
    path("our-members", views.OurMembersView.as_view(), name="our-members"),
    path("our-members/<int:id>", views.OurMembersDetialView.as_view(),
         name="our-members-details"),
    path("advertisement", views.AdvertismentView.as_view(), name="advertisement"),
    path("advertisement/<int:id>", views.AdvertistmentDetailedView.as_view(),
         name="advertisement-detailed"),


    # PUBLIC URLS
    path("why-join/public", views.WhyJoinManPublicView.as_view(),
         name="why-join-public"),
    path("join-step/public", views.JoiningStepPublicView.as_view(),
         name="join-step-public"),
    path("faq/public", views.FAQsPublicView.as_view(), name="faq-public"),
    path("why-we-are-unique/public", views.WhyWeAreUniquePublicView.as_view(),
         name="why-we-are-unique-public"),
    path("our-members/public", views.OurMembersPublicView.as_view(),
         name="our-members-public"),
    path("advertisement-public", views.AdvertisementPublicView.as_view(),
         name="advertisement-public")
]
