from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("inscription/", views.RegisterView.as_view(), name="register"),
    path("connexion/", views.LoginView.as_view(), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("email/verifier/<uidb64>/<token>/", views.VerifyEmailView.as_view(), name="verify-email"),
    path("mot-de-passe/oublie/", views.ForgotPasswordView.as_view(), name="password-reset"),
    path("mot-de-passe/reinitialiser/<uidb64>/<token>/", views.ResetPasswordConfirmView.as_view(), name="password-reset-confirm"),
    path("mot-de-passe/reinitialiser/termine/", views.ResetPasswordCompleteView.as_view(), name="password-reset-complete"),
    path("mot-de-passe/modifier/", views.change_password_view, name="change-password"),
]