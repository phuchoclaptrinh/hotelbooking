from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    user_form = forms.CharField(label='Email hoặc số điện thoại')