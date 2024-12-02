from django import forms
from movies.models import Movie
from cinema.models import Cinema, ScheduledMovie
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime

CustomUser = get_user_model()

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-base', 
            'placeholder': 'Enter your email',
        }),
        error_messages={'required': 'Email field must be provided'},
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-base',   
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
    movie_name = forms.CharField(
        label="Movie Name",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter movie name'
        })
    )
    
    director = forms.CharField(
        label="Director",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter director name'
        })
    )
    
    producer = forms.CharField(
        label="Producer",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter producer name'
        })
    )
    
    synopsis = forms.CharField(
        label="Synopsis",
        max_length = 1000,
        widget=forms.Textarea(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm resize-none',
            'placeholder': 'Enter movie synopsis', 
            'rows': 4
        })
    )
    
    cast = forms.CharField(
        label="Cast",
        widget=forms.Textarea(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm resize-none',
            'placeholder': 'Enter cast members', 
            'rows': 3
        })
    )
    
    duration = forms.DurationField(
        label="Duration (HH:MM:SS)",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter duration (e.g. HH:MM:SS)'
        })
    )
    
    movie_format = forms.ChoiceField(
        label="Format",
        choices=[('3D', '3D'), ('2D', '2D')],
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
        })
    )
    
    movie_rating = forms.ChoiceField(
        label="Rating",
        choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R')],
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
        })
    )
    
    genre = forms.CharField(
        label="Genre",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter genre'
        })
    )

    class Meta:
        model = Movie
        fields = '__all__'  # Still using this to include all fields from the Movie model

class AddNowShowingMovieForm(forms.Form):
    cinema = forms.ChoiceField(
        label="Select Cinema",
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'autocomplete': 'off'
        })
    )
    
    movie = forms.ChoiceField(
        label="Select Movie",
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'autocomplete': 'off'
        })
    )
    
    
    end_date = forms.DateTimeField(
        label="Showing End Date",
        widget=forms.DateTimeInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Username',
            'autocomplete': 'off',
            'type': 'datetime-local'  
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Query the Movie model to get the movies
        self.set_movie_choices()
        self.set_cinema_choices()
    
    def set_movie_choices(self):
        movie_choices = Movie.objects.values_list("id", "movie_name")  # Adjust field names accordingly
        self.fields["movie"].choices = movie_choices
    
    def set_cinema_choices(self):
        cinema_choices = Cinema.objects.values_list("id", "cinema_name")
        self.fields["cinema"].choices = cinema_choices
    
class AddCinemaForm(forms.ModelForm):
    cinema_name = forms.CharField(
        label="Cinema Name",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-base',   
            'placeholder': 'Enter cinema name',
        })
    )
    
    capacity = forms.CharField(
        label="Capacity",
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-base',   
            'placeholder': 'Enter cinema capacity',
            'min': '0'
        })
    )
    
    class Meta:
        model = Cinema
        fields = "__all__"

    
    def clean(self):
        cleaned_data = super().clean()
        cinema_name = cleaned_data.get('cinema_name')

        # Check if cinema name is already taken
        if cinema_name and Cinema.objects.filter(cinema_name=cinema_name).exists():
            self.add_error(None, "This cinema name is already taken. Please try a different name.")

        return cleaned_data

class AddScheduledMovieForm(forms.Form):
    movie = forms.ChoiceField(
        label="Select a Movie",
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 max-h-48 overflow-y-auto',
            'autocomplete': 'off'
        })
    )
    
    cinema = forms.ChoiceField(
        label="Select a Cinema",
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 max-h-48 overflow-y-auto',
            'autocomplete': 'off'
        })
    )
    
    schedule = forms.DateTimeField(
        label="Movie Schedule",
        widget=forms.DateTimeInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter Username',
            'autocomplete': 'off',
            'type': 'datetime-local',
            'title': "Choose date and time for movie schedule",
            'min': datetime.now().strftime("%Y-%m-%dT%H:%M")
        })
    )
    
    audience_number = forms.CharField(
        label="Audience Number",
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-gray-300 p-2 text-base',   
            'min': '0',
            'step': '1',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Query the Movie model to get the movies
        self.set_movie_to_show()
        self.set_cinema_choices()
    
    def set_movie_to_show(self):
        movies = Movie.objects.all()
        
        choices = [
            (movie.id, movie.movie_name) for movie in movies
        ]
        
        self.fields["movie"].choices = choices
    
    def set_cinema_choices(self):
        cinema_list = Cinema.objects.all()
        
        choices = [
            (cinema.id, cinema.cinema_name) for cinema in cinema_list
        ]
        
        self.fields["cinema"].choices = choices
        
class AddTicketForm(forms.Form):
    user = forms.ChoiceField(
        label="Select a User",
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'autocomplete': 'off'
        })
    )
    
    scheduled_movie = forms.ChoiceField(
        label="Select a Scheduled Movie",
        widget=forms.Select(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'autocomplete': 'off'
        })
    )
    
    seat_identifier = forms.CharField(
        label="Seat Identifier",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 p-2 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Enter seat identifier'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Query the Movie model to get the movies
        self.set_user_choices()
        self.set_scheduled_movie_choices()
        
    def set_user_choices(self):
        users = CustomUser.objects.all()
        
        choices = [
            (user.id, f"{user.first_name} {user.last_name}") for user in users
        ]
        
        self.fields["user"].choices = choices
    
    def set_scheduled_movie_choices(self):
        scheduled_movies = ScheduledMovie.objects.select_related('cinema', 'movie').filter(is_active=True)
        
        choices = [
            (sm.id, f"{sm.cinema.cinema_name} - {sm.movie.movie_name}") for sm in scheduled_movies
        ]
        
        self.fields["scheduled_movie"].choices = choices
        