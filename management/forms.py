from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import ThingsboardCredentials, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class UserProfileForm(forms.ModelForm):
    thingsboard_username = forms.CharField(
        required=False, help_text="Stored for Thingsboard data pulls."
    )
    thingsboard_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Stored for Thingsboard data pulls.",
    )
    thingsboard_access_token = forms.CharField(
        required=False,
        help_text="Thingsboard access token (preferred for scheduled pulls).",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        creds = getattr(self.instance, "thingsboard_credentials", None)
        if creds:
            self.fields["thingsboard_username"].initial = creds.thingsboard_username
            self.fields["thingsboard_password"].initial = creds.thingsboard_password
            self.fields[
                "thingsboard_access_token"
            ].initial = creds.thingsboard_access_token

    def save(self, commit=True):
        user = super().save(commit=commit)
        creds, _ = ThingsboardCredentials.objects.get_or_create(user=user)
        creds.thingsboard_username = self.cleaned_data.get("thingsboard_username")
        creds.thingsboard_password = self.cleaned_data.get("thingsboard_password")
        creds.thingsboard_access_token = self.cleaned_data.get(
            "thingsboard_access_token"
        )
        creds.save()
        return user
