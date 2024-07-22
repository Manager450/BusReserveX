# reservations/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BusSearchForm(forms.Form):
    from_location = forms.CharField(max_length=100)
    to_location = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.SelectDateWidget)

class PasswordChangeCustomForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 != new_password2:
            raise forms.ValidationError("The new passwords do not match.")

        # Check password guidelines
        if len(new_password1) < 8:
            raise forms.ValidationError("The new password must be at least 8 characters long.")
        if not any(char.isdigit() for char in new_password1):
            raise forms.ValidationError("The new password must contain at least one digit.")
        if not any(char.isalpha() for char in new_password1):
            raise forms.ValidationError("The new password must contain at least one letter.")

