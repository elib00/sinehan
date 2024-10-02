from django import forms
from movies.models import Movie
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AdminLoginForm(forms.Form):
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


class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
            'movie_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter movie name'
            }),
            'director': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter director name'
            }),
            'producer': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter producer name'
            }),
            'synopsis': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter movie synopsis', 
                'rows': 5
            }),
            'cast': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter cast members', 
                'rows': 3
            }),
            'duration': forms.TimeInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter duration (e.g. HH:MM:SS)'
            }),
            'movie_format': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none'
            }),
            'movie_rating': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none'
            }),
            'genre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none', 
                'placeholder': 'Enter genre'
            }),
        }