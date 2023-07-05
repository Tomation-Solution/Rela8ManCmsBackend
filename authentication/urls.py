from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login", views.LoginUserView.as_view(), name="login"),
    path("logout", views.LogoutUserView.as_view(), name="logout"),#This isn't to be used
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', views.LogoutUserView.as_view(),
         name='token_blacklist'),
    path('create-account/',views.CreateAccount.as_view(),name='create-account'),
]
