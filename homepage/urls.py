# Update your urls.py file to include footer management

from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register("add-slider", views.HomePageSliderViewset, basename="homepageslider")
route.register("footer", views.FooterContentViewset, basename="footercontent")

urlpatterns = [] + route.urls

# This will create the following endpoints:
# GET/POST    /footer/                    - List/Create footer content
# GET/PUT/PATCH/DELETE /footer/{id}/     - Retrieve/Update/Delete footer content
# GET         /footer/content/            - Public endpoint to get footer content
# PATCH       /footer/update_content/     - Update footer content
