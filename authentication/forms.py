from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from validators import validate_password, validate_names
from .models import CustomUser

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True, label="First name", validators=[validate_names])
    middle_name = forms.CharField(max_length=20, label="Middle name", validators=[validate_names], required=False)
    last_name = forms.CharField(max_length=20, required=True, label="Last name", validators=[validate_names])
    email = forms.EmailField(validators=[validate_email], required=True, max_length=100, label="Email")
    password1 = forms.CharField(max_length=128, label="Password", required=True, validators=[validate_password],
                               widget=forms.PasswordInput)
    role = forms.ChoiceField(label="Role", choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "middle_name", "email", "password1", "password2", "role")


class AuthoriseForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100, label="Email")
    password = forms.CharField(max_length=128, label="Password", required=True, widget=forms.PasswordInput)
