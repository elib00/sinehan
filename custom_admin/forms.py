from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-lg', 
            'placeholder': 'Enter your email',
        }),
        error_messages={'required': 'Email field must be provided'},
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-lg',   
            'placeholder': 'Enter your password',
        }),
        error_messages={'required': 'Password field must be provided'},
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email field must be provided")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password field must be provided")
        return password

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not CustomUser.objects.filter(email=email).exists():
            self.add_error("email", "User with this email does not exist.")
        
        return cleaned_data
