from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import ThingsboardCredentials, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ThingsboardCredentialsForm(forms.ModelForm):
    thingsboard_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Stored for Thingsboard data pulls.",
    )

    class Meta:
        model = ThingsboardCredentials
        fields = (
            "thingsboard_username",
            "thingsboard_password",
            "thingsboard_access_token",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure empty string initial when no values
        for name in self.fields:
            self.fields[name].initial = self.initial.get(name, "") or ""
