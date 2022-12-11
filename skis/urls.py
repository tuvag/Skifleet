from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views, forms

urlpatterns = [
    #ski views
    path("", views.SkiSearchList.as_view(), name="index"),
    path("addski", views.SkiCreateView.as_view(), name="addski"),
    path("ski_details/<int:id>", views.ski_details, name="ski-details"),
    path("update_ski/<int:pk>", views.SkiUpdateView.as_view(), name="update-ski"),
    path("delete_ski/<int:pk>", views.SkiDeleteView.as_view(), name="delete-ski"),

    #setting views
    path("setting", views.SettingSearchList.as_view(), name="setting"),
    path("setting_details/<int:id>", views.setting_details, name="setting-details"),
    path("addskitest", views.SettingCreateView.as_view(), name="addskitest"),
    path("update_setting/<int:pk>", views.SettingUpdateView.as_view(), name="update-setting"),
    path("delete_setting/<int:pk>", views.SettingDeleteView.as_view(), name="delete-setting"),
    
    #contact views
    path("contact", views.contact, name="contact"),
    path("thanks", views.thanks, name="thanks"),

    # login views
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("register", views.register, name="register"),
    path("password_change", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=forms.MyPasswordResetForm), name='password_reset'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)