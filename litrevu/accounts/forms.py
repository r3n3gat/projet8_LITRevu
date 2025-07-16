from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SignUpForm(UserCreationForm):
    """
    Formulaire d'inscription : ne demande que le username et les mots de passe.
    """
    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': _("Nom d’utilisateur"),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulaire de connexion, labels en français et widgets accessibles.
    """
    username = forms.CharField(
        label=_("Nom d’utilisateur"),
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password'
        })
    )


class ProfileForm(forms.ModelForm):
    """
    Pour modifier son profil : username, email, bio.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'bio')
        labels = {
            'username': _("Nom d’utilisateur"),
            'email': _("Email"),
            'bio': _("Bio"),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
