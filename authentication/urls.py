# urls.py
from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login", views.LoginUserView.as_view(), name="login"),
    path(
        "logout", views.LogoutUserView.as_view(), name="logout"
    ),  # This isn't to be used
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", views.LogoutUserView.as_view(), name="token_blacklist"),
    path("create-account/", views.CreateAccount.as_view(), name="create-account"),
    # New URLs to support frontend functionality
    path("admins/", views.AdminListView.as_view(), name="admin-list"),
    path("admin/<int:pk>", views.AdminDetailView.as_view(), name="admin-detail"),
    path(
        "password-reset/request/",
        views.RequestPasswordResetView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        views.ResetPasswordConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "admin/password-reset/",
        views.AdminPasswordResetView.as_view(),
        name="admin-password-reset",
    ),
]
