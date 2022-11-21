from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("", views.SkiListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("contact", views.contact, name="contact"),
    path("addski", views.SkiCreateView.as_view(), name="addski"),
    path("add_skitest", views.add_skitest, name="add_skitest"),
    path("skitest", views.skitest, name="skitest"),
]