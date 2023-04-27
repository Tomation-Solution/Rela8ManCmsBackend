from django.urls import path
from aboutus import views

urlpatterns = [
    # CONTACT US ENDPOINTS
    path("contact", views.AboutContactUsView.as_view(), name="about-contact"),
    path("contact/<int:id>", views.AboutContactUsDetailsView.as_view(),
         name="about-contact-delete"),

    # About History Enpoints
    path("history", views.AboutHistoryView.as_view(), name="about-history"),

    # About Advocacy Endpoints
    path("advocacy", views.AboutAdvocacyView.as_view(), name="about-advocacy"),

    # About Affilliate Endpoints
    path("affilliate", views.AboutAffilliateView.as_view(), name="about-affilliate"),

    # About How We Work Endpoints
    path("how-we-work", views.AboutHowWeWorkView.as_view(),
         name="about-how-we-work"),

    # About Where We Operate Endpoints
    path("how-we-operate", views.AboutWhereWeOperatView.as_view(),
         name="about-how-we-operate"),

    # About Where We Operate Office Endpoints
    path("how-we-operate/office",
         views.AboutWhereWeOperateOfficeViews.as_view(), name="operate-office"),
    path("how-we-operate/office/<int:id>",
         views.AboutWhereWeOperateOfficeDetailViews.as_view(), name="operate-office-details"),

    # About Where We Operate Branch Endpoints
    path("how-we-operate/branch",
         views.AboutWhereWeOperateBranchViews.as_view(), name="operate-branch"),
    path("how-we-operate/branch/<int:id>",
         views.AboutWhereWeOperateBranchDetailsViews.as_view(), name="operate-branch-details"),
     path("our-executives", views.AboutOurExecutivesViews.as_view(),name="our-executives"),
     path("our-executives/<int:id>", views.AboutOurExecutivesDetailViews.as_view(), name="our-executives-details"),


    # PUBLIC VIEWS
    # About Where We Operate Branch Endpoints
    path("how-we-operate/branch/public",
         views.AboutWhereWeOperateBranchPublicViews.as_view(), name="operate-branch-public"),

    # About Where We Operate Office Endpoints
    path("how-we-operate/office/public",
         views.AboutWhereWeOperateOfficePublicViews.as_view(), name="operate-office-public"),

     path("our-executives/public", views.AboutOurExecutivesPublicView.as_view(),name="our-executives-public"),
]
