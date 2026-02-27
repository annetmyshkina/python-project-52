
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class BaseUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("First name"),
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": _("Enter your first name")
                                      })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Last name"),
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": _("Enter your last name")
                                      })
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        label=_("Username"),
        validators=[RegexValidator(r"^[\w.@+-]+$", _("Invalid characters"))],
        widget=forms.TextInput(attrs={"class": "form-control",
                                      "placeholder": _("Enter username")
                                      }),
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    )

    class Meta:
        model = User
        fields = []

    def clean_username(self):
            username = self.cleaned_data["username"]
            queryset = User.objects.filter(username__iexact=username)

            if hasattr(self, "instance") and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise ValidationError(_("Username already taken."))

            return username


class CustomUserCreationForm(BaseUserForm, UserCreationForm):

    class Meta(BaseUserForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = _("Password")
        self.fields["password1"].help_text = _("Your password must contain at least 8 characters.")

        self.fields["password2"].label = _("Confirm password")
        self.fields["password2"].help_text = _("Please enter the password again to confirm.")


class CustomUserChangeForm(BaseUserForm, UserChangeForm):
    password = None

    class Meta(BaseUserForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")


class UserDeleteForm(forms.ModelForm):
    confirm = forms.BooleanField(
        required=True,
        label=_("I confirm this action is irreversible"),
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = User
        fields = ["confirm"]

