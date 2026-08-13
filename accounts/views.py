from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from .forms import ForgotPasswordForm, LoginForm, RegisterForm
from .tasks import send_activation_email_task, send_password_reset_email_task
from .tokens import email_verification_token

# Create your views here.

User = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(User)
        activation_link = self.request.build_absolute_uri(
            reverse("accounts:verify-email", kwargs={"uidb64": uid, "token": token})
        )

        send_activation_email_task.delay(user.id, activation_link)

        return render(self.request, "accounts/verify_email_sent.html", {"email": user.email})


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(User, token):
            user.is_active = True
            user.is_email_verified = True
            user.save(update_fields=["is_active", "is_email_verified"])
            messages.success(
                request,
                "Votre adresse e mail a ete verifie. Vous pouvez maintenant vous connecter"
            )
            return redirect("accounts:login")

        return render(request, "accounts/verify_email_invalid.html")

class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class ForgotPasswordView(FormView):
    form_class = ForgotPasswordForm
    template_name = "accounts/forgot_password.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email__iexact=email, is_active=True)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = self.request.build_absolute_uri(
            reverse("accounts:password-reset-confirm", kwargs={"uidb64": uid, "token": token})
        )

        send_password_reset_email_task.delay(user.id, reset_link)

        return render(self.request, "accounts/forgot_password_done.html", {"email": user.email})

class ResetPasswordConfirmView(View):
    def _get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token):
        user = self._get_user(uidb64)
        if user is None or not default_token_generator.check_token(user, token):
            return render(request, "accounts/reset_password_invalid.html")

        form = SetPasswordForm(user)
        return render(request, "accounts/reset_password_confirm.html", {"form":form})

    def post(self, request, uidb64, token):
        user = self._get_user(uidb64)
        if user is None or not default_token_generator.check_token(user, token):
            return render(request, "accounts/reset_password_invalid.html")

        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:password-reset-complete")
        return render(request, "accounts/reset_password_confirm.html", {"form": form})

class ResetPasswordCompleteView(TemplateView):
    template_name = "accounts/reset_password_complete.html"


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request.user)
            messages.success(request, "Votre mot de passe a ete modifie avec succes")
            return redirect("accounts:change-password")
        else:
            form = PasswordChangeForm(request.user)
        return render(request, "accounts/change_password.html", {"form" : form})