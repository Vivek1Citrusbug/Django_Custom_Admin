import re
from typing import Any, Dict

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("Please enter a correct %(username)s and password."),
        "inactive": _("This account is inactive."),
    }


class CreateUserForm(ModelForm):

    confirm_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "username",
            "is_active",
            "confirm_password",
        ]

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        username = cleaned_data.get("username")
        confirm_password = cleaned_data.get("confirm_password")

        if username and settings.USER_NAME_REGEX:
            if not re.match(settings.USER_NAME_REGEX, username):
                raise forms.ValidationError(
                    {"username": "Please enter a valid username"}
                )

        if email and settings.EMAIL_REGEX:
            if not re.match(settings.EMAIL_REGEX, email):
                raise forms.ValidationError({"email": "Please enter a valid email"})

        if password and settings.PASSWORD_REGEX:
            if not re.match(settings.PASSWORD_REGEX, password):
                raise forms.ValidationError(
                    {"password": "Please enter a strong password"}
                )

        if confirm_password != password:
            raise forms.ValidationError(
                {"confirm_password": "The provided password does not match."}
            )

        return cleaned_data


class UpdateUserForm(ModelForm):

    username = forms.EmailField(disabled=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance