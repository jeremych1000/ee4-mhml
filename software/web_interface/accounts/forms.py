from django import forms
from django.contrib.auth.models import User

from accounts.models import UserProfile
from passwords.fields import PasswordField
from accounts.models import TestPost

class UserForm(forms.ModelForm):
    #password = forms.CharField(label='Password',
    #                           max_length=30,
    #                           widget = forms.PasswordInput())
    first_name = forms.CharField(label="First name",
                               max_length=30,
                               widget=forms.TextInput(attrs={
                                   'name': 'first_name'
                               }))
    last_name = forms.CharField(label="Last name",
                               max_length=30,
                               widget=forms.TextInput(attrs={
                                   'name': 'last_name'
                               }))
    password = PasswordField(label='Password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email', )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class TestPostForm(forms.ModelForm):
    class Meta:
        model = TestPost
        fields = ('post_data',)

