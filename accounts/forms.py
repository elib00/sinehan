from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Username',
            'autocomplete': 'off'
        })
    )
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Email',
            'autocomplete': 'off'
        })
    )
    
    first_name = forms.CharField(
        label="Firstname",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Firstname',
            'autocomplete': 'off'
        })
    )
    
    last_name = forms.CharField(
        label="Lastname",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Lastname',
            'autocomplete': 'off'
        })
    )
    
    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.DateInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Date of Birth',
            'type': 'date'  # This ensures the input type is date for HTML5 date picker
        })
    )
        
    address = forms.CharField(
        label="Address",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Address',
            'autocomplete': 'off'
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your password',
            'autocomplete': 'off'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 xrounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your password again',
            'autocomplete': 'off'
        })
    )

    #TODO clean_password2 na method, need sha i override aron maka non-field error ta
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'address', 'password1', 'password2']

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'address']
