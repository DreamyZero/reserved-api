from django.contrib.auth.forms import AuthenticationForm
from django import forms


class AuthorizationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.PasswordInput()
