# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=25)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
