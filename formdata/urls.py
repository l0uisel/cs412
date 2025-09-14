# file: formdata/urls.pw

from django.urls import path  # from django urls library
from django.conf import settings  # include installed apps
from . import views  # from . = local directory

# URL patterns specific to the hw app:
# variable name django looks for
urlpatterns = [
    path(r"", views.show_form, name="show_form"),
    path(r"submit", views.submit, name="submit"),
    # path(r"", views.home, name="home"),  # connects empty string to views.home
    # path(r"", views.home_page, name="home_page"),
    # path(r"about", views.about, name="about_page"),
]
