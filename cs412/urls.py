# file: cs412/urls.py
# author: Louise Lee, llouise@bu.edu, 09/07/2025
# description: root URL configuration for cs412 project.
# maps URL paths from apps and set up static file for development.

"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

# Routes beginning with /" "/ go to the " " app
urlpatterns = [
    path("admin/", admin.site.urls),
    path("hw/", include("hw.urls")),  # refer anything with spring hw/ to hw app
    path(
        "quotes/", include("quotes.urls")
    ),  # refer anything with spring quotes/ to quotes app
    path(
        "formdata/", include("formdata.urls")
    ),  # refer anything with spring formdata/ to formdata app
    path(
        "restaurant/", include("restaurant.urls")
    ),  # refer anything with spring restaurant/ to restaurant app
    path("blog/", include("blog.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Serve static files during development
