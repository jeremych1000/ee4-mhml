from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User

from accounts.models import UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               max_length=30,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'name': 'username'
                               }))
    password = forms.CharField(label="Password",
                                     max_length=30,
                                     widget=forms.PasswordInput(attrs={
                                         'class': 'form-control',
                                         'name': 'password'
                                     }))

class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               max_length=30,
                               widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)



