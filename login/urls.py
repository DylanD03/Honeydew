from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("logout/", views.logoutRequest, name="logoutRequest"),
    path("signup/", views.signup, name="signup-page"),
    path("submit-signup-credentials/", views.submit_signup_credentials, name="signup"),
    path("submit-login-credentials/", views.submit_login_credentials, name="submit-login"),
]
