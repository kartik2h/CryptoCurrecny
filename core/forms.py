from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        error_messages={'required': ''}
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'required': ''}
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        error_messages={'required': '', 'password_mismatch': ''}

    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}),
        error_messages={'required': ''}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(
        label='Upload Profile Picture')

    class Meta:
        model = UserProfile
        fields = ['profile_pic']
