from django.urls import path
from django.contrib.auth .views import LoginView, LogoutView
from .views import signup, activate, password_change, user_withdrawal, find_id, find_password, reset_password

app_name = "accounts"
urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path("withdrawal/", user_withdrawal, name="withdrawal"),
    path("signup/", signup, name="signup"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password/', password_change, name='password_change'),
    path("find_account/", find_id, name="find_id"),
    path("find_passwd/", find_password, name="find_password"),
    path("reset_passwd/<uidb64>/<token>/",
         reset_password, name="reset_password"),
]
