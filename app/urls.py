"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include("authentication.urls")),  # done done
    path("api/publications/", include("publications.urls")),  # done done
    path("api/news/", include("news.urls")),  # done done
    path("api/gallery/", include("gallery.urls")), # done
    path("api/reports/", include("reports.urls")),  # done done
    path("api/events/", include("events.urls")),  # done done
    path("api/trainings/", include("trainings.urls")),  # done done
    path("api/aboutus/", include("aboutus.urls")),  # done 
    path("api/services/", include("services.urls")), # done done
    path("api/membership/", include("membership.urls")),  # done done
    path("api/structure/", include("structure.urls")),
    path("api/payments/", include("payments.urls")),
]
