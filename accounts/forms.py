from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est deja utilisee par un autre compte")
        return email

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Ce compte n'est pas encore active alors verifie ta boite email et cliquez sur le lien de confirmation",
                code="inactive",
            )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Adresse e-mail')
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Aucun compte actif n'est associe a cette adress e-mail")
        return email