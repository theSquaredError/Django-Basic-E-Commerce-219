from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput

from home.models import Contact


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email','username',  'password1', 'password2' )
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name','help_text':'Optional.'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'Last Name','help_text':'Optional.'}),
            'email'     : TextInput(attrs={'class': 'input','placeholder':'Email', 'help_text':'Required. Inform a valid email address.'}),
            'username'  : TextInput(attrs={'class': 'input','placeholder':'Username'}),
            'password1' : TextInput(attrs={'class': 'input', 'type': 'password'}),
            'password2' : TextInput(attrs={'class': 'input', 'type': 'password'}),
        }


class UserUpdeteForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email','username',)
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name','help_text':'Optional.'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'Last Name','help_text':'Optional.'}),
            'email'     : TextInput(attrs={'class': 'input','placeholder':'Email', 'help_text':'Required. Inform a valid email address.'}),
            'username'  : TextInput(attrs={'class': 'input','placeholder':'Username'}),
        }