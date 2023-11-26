from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, ContactMessage, OrderHistory, Feedback


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
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class OrderHistoryForm:
    class Meta:
        model = OrderHistory
        fields = ['user', 'name', 'email', 'transaction_date', 'price']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'first_visit', 'found_needed', 'reason', 'ease_of_use', 'likelihood_to_return', 'comments']

    # Updated fields with choices
    first_visit = forms.ChoiceField(
        choices=[('', 'Select an option')] + Feedback.FIRST_VISIT_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    found_needed = forms.ChoiceField(
        choices=[('', 'Select an option')] + Feedback.FOUND_NEEDED_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    reason = forms.ChoiceField(
        choices=[('', 'Select an option')] + Feedback.REASON_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    ease_of_use = forms.ChoiceField(
        choices=[('', 'Select an option')] + Feedback.EASE_OF_USE_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    likelihood_to_return = forms.ChoiceField(
        choices=[('', 'Select an option')] + Feedback.LIKELIHOOD_TO_RETURN_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

