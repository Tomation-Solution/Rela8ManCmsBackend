from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register('add-slider',views.HomePageSliderViewset)
urlpatterns =[

] + route.urls