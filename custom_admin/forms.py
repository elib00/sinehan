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

from django import forms
from movies.models import Movie

class AddMovieForm(forms.ModelForm):
    movie_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter movie name'
        })
    )
    
    director = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter director name'
        })
    )
    
    producer = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter producer name'
        })
    )
    
    synopsis = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter movie synopsis', 
            'rows': 5
        })
    )
    
    cast = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter cast members', 
            'rows': 3
        })
    )
    
    duration = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter duration (e.g. HH:MM:SS)'
        })
    )
    
    movie_format = forms.ChoiceField(
        choices=[('format1', 'Format 1'), ('format2', 'Format 2')],  # Update with actual choices
        widget=forms.Select(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full'
        })
    )
    
    movie_rating = forms.ChoiceField(
        choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R')],  # Update with actual choices
        widget=forms.Select(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full'
        })
    )
    
    genre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg p-2 w-full', 
            'placeholder': 'Enter genre'
        })
    )

    class Meta:
        model = Movie
        fields = '__all__'  # Still using this to include all fields from the Movie model
