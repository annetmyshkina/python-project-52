from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserFieldsMixin:
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("First name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your first name"),
            }
        ),
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Last name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your last name"),
            }
        ),
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        label=_("Username"),
        validators=[RegexValidator(r"^[\w.@+-]+$", _("Invalid characters"))],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter username"),
            }
        ),
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
    )


class CustomUserCreationForm(UserFieldsMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserFieldsMixin, UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )


class UserDeleteForm(forms.ModelForm):
    confirm = forms.BooleanField(
        required=True,
        label=_("I confirm this action is irreversible"),
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = User
        fields = ("confirm",)
