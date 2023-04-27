from django.urls import path
from reports import views

urlpatterns = [
    path("", views.ReportsView.as_view(), name="report"),
    path("<int:id>", views.ReportsDetialView.as_view(), name="reports"),
    path("public", views.ReportsViewPublic.as_view(), name="report-public"),
]
