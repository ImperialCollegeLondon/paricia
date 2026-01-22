from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class UserProfileForm(forms.ModelForm):
    thingsboard_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Stored for Thingsboard data pulls.",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "thingsboard_username",
            "thingsboard_password",
            "thingsboard_access_token",
        )
