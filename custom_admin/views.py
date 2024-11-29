from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseForbidden
from .forms import AdminLoginForm, AddMovieForm, AddCinemaForm, AddScheduledMovieForm, AddTicketForm
from cinema.models import Cinema, Ticket, ScheduledMovie
from movies.models import Movie
from accounts.forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Prefetch
import json

CustomUser = get_user_model()

# Create your views here.
class AdminLoginView(View):
    def get(self, request):
        form = AdminLoginForm()
        return render(request, "pages/login.html", {"form": form})

    def post(self, request):
        form = AdminLoginForm(request.POST)  
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_superuser and user.is_staff:
                    login(request, user)
                    messages.success(request, "User logged in successfully!")
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "User lacks the necessary access permissions")
                    form.add_error(None, "User must be an admin to access this page")
            else:
                messages.error(request, "Incorrect password")
                form.add_error("password", "Incorrect password")
        else:
            print(form.errors)
            messages.error(request, "User authentication failed")
            
        return render(request, "pages/login.html", {"form": form})

class AdminDashboardView(LoginRequiredMixin, View):
    #TODO ig get sa dashboard kay mo generate sha sa mga forms na needed 
    
    login_url = "/admin/login/"  # Specify the login URL here
    redirect_field_name = "next"  # This is the default field to redirect after login
    
    def get(self, request): 
        add_movie_form = AddMovieForm()
        
        context = {
            "add_movie_form": add_movie_form
        }
        
        return render(request, "pages/dashboard.html", context)

    def post(self, request):
        form_type = request.POST.get("form_type")
    
        if form_type == "add_movie":
            return self.process_add_movie(request)
        
    def process_add_movie(self, request):
        form = AddMovieForm(request.POST)
        if form.is_valid():
            form.save()
            print("na save ang movie")
            return redirect("admin_dashboard")
        else:
            print(form.errors)

        return render(request, "pages/dashboard.html", {"add_movie_form": form})

# TODO handle ang pag add og movie logic
class AdminDashboardAddUserView(View):
    def get(self, request):
        add_movie_form = AddMovieForm()
        add_user_form = CustomUserCreationForm()
        
        context = {
            "add_movie_form": add_movie_form,
            "add_user_form": add_user_form
        }
        
        return render(request, "sections/add_user.html", context)
        
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "User creation failed")
            print(form.errors)
        
        return render(request, "sections/add_user.html", {"add_user_form": form})

class AdminDashboardUpdateUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        print(user_id)
        form = CustomUserUpdateForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect("admin_dashboard_all_users")
        else:
            messages.error(request, "User update unsuccessful")
            print(form.errors)
        
        return render(request, "sections/all_users.html", {"update_user_form": form})
        
class AdminDashboardAllUsersView(View):
    def get(self, request):
        add_movie_form = AddMovieForm()
        update_user_form = CustomUserUpdateForm()
        users = CustomUser.objects.all()
        
        context = {
            "users": users,
            "add_movie_form": add_movie_form,
            "update_user_form": update_user_form
        }
        
        return render(request, "sections/all_users.html", context)

class AdminDashboardMovieListView(View):
    def get(self, request):
        add_movie_form = AddMovieForm()
        movies = Movie.objects.all()
        
        context = {
            "add_movie_form": add_movie_form,
            "movies": movies
        }
        
        return render(request, "sections/movie_list.html", context)

class AdminDashboardAddMovieView(View):
    def post(self, request):
        movies = Movie.objects.all()
        add_movie_form = AddMovieForm(request.POST)
        if add_movie_form.is_valid():
            add_movie_form.save()
            messages.success(request, "A new movie has been added!")
            return redirect("admin_dashboard_movie_list")
        else:
            print(add_movie_form.errors)
            messages.error(request, "Failed to add new movie")

        context = {
            "add_movie_form": add_movie_form,
            "movies": movies
        }
        
        return render(request, "sections/movie_list.html", context)
        

class AdminLogoutView(LogoutView):
    next_page = reverse_lazy("admin_login")
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Logout successful!")
        return response
    
class AdminDashboardTicketsView(View):
    def get(self, request):
        add_ticket_form = AddTicketForm()
        context = self.init_context()
        
        context["add_ticket_form"] = add_ticket_form
        return render(request, "sections/tickets.html", context)

    def init_context(self):
        #for displaying by scheduled_movie
        scheduled_movies = ScheduledMovie.objects.select_related("movie").prefetch_related("movie_tickets__user").all()
        
        #for displaying by tickets only
        tickets = Ticket.objects.select_related("user", "scheduled_movie__movie", "scheduled_movie__cinema").all()
        for ticket in tickets:
            ticket.available_seats = ticket.scheduled_movie.cinema.capacity - ticket.scheduled_movie.audience_number
        
        #for displaying by users
        users = CustomUser.objects.prefetch_related("user_tickets__scheduled_movie__movie", "user_tickets__scheduled_movie__cinema").all()
        
        #json for dynamic content with js
        tickets_data = [
            {
                'ticket_id': ticket.id,
                'ticket_is_active': ticket.is_active,
                'user_id': ticket.user.id,  # You might want to include specific fields from related models
                'user_first_name': ticket.user.first_name,
                'user_last_name': ticket.user.last_name,
                'user_email': ticket.user.email,
                'scheduled_movie_id': ticket.scheduled_movie.id,
                'scheduled_movie_movie_name': ticket.scheduled_movie.movie.movie_name,
                'scheduled_movie_cinema_id': ticket.scheduled_movie.cinema.id,
                'scheduled_movie_cinema_name': ticket.scheduled_movie.cinema.cinema_name,
                'scheduled_movie_date': ticket.scheduled_movie.schedule.strftime('%B %d, %Y'),
                'scheduled_movie_time': ticket.scheduled_movie.schedule.strftime('%I:%M:%S %p'),  # Time only
                'available_seats': ticket.available_seats,
                'seat_identifier': ticket.seat_identifier
            }
            for ticket in tickets
        ]
        
        # scheduled_movies = ScheduledMovie.objects.select_related("movie").prefetch_related("movie_tickets").all()
        scheduled_movie_data = [
            {
                'scheduled_movie_id': scheduled_movie.id,
                'scheduled_movie_is_active': scheduled_movie.is_active,
                'scheduled_movie_movie_name': scheduled_movie.movie.movie_name,
                'scheduled_movie_date': scheduled_movie.schedule.strftime('%B %d, %Y'),  # Date only
                'scheduled_movie_time': scheduled_movie.schedule.strftime('%I:%M:%S %p'),  # Time only
                'scheduled_movie_cinema_name': scheduled_movie.cinema.cinema_name,
                'scheduled_movie_available_seats': scheduled_movie.cinema.capacity - scheduled_movie.audience_number,
                'scheduled_movie_tickets': [
                    {
                        'ticket_id': ticket.id,
                        'ticket_seat_identifier': ticket.seat_identifier,
                        'ticket_holder': f"{ticket.user.first_name} {ticket.user.last_name}",
                        'ticket_holder_username': ticket.user.username,
                        'ticket_is_active': "Active" if ticket.is_active else "Inactive"
                    }
                    for ticket in scheduled_movie.movie_tickets.all()  # Iterate over related tickets
                ]
            }
            for scheduled_movie in scheduled_movies
            
        ]
        
        # users = CustomUser.objects.prefetch_related("user_tickets__scheduled_movie__movie", "user_tickets__scheduled_movie__cinema").all()
        users_data = [
            {
                'user_id': user.id,
                'user_first_name': user.first_name,
                'user_last_name': user.last_name,
                'user_username': user.username,
                'user_email': user.email,
                'user_tickets': [
                    {
                        'ticket_id': ticket.id,
                        'ticket_seat_identifier': ticket.seat_identifier,
                        'ticket_is_active': ticket.is_active,
                        'ticket_scheduled_movie_movie_name': ticket.scheduled_movie.movie.movie_name,
                        'ticket_scheduled_movie_date': ticket.scheduled_movie.schedule.strftime('%B %d, %Y'),
                        'ticket_scheduled_movie_time': ticket.scheduled_movie.schedule.strftime('%I:%M:%S %p'),
                        'ticket_cinema_cinema_name': ticket.scheduled_movie.cinema.cinema_name
                    }

                    for ticket in user.user_tickets.all() # Iterate over related tickets
                ] 
                   
            }
            for user in users
        ]
    
        # Serialize the data to JSON
        tickets_json = json.dumps(tickets_data)
        scheduled_movie_json = json.dumps(scheduled_movie_data)
        users_json = json.dumps(users_data)

        # print(tickets_json)

        
        context = {
            "scheduled_movies": scheduled_movies,
            "tickets": tickets,
            "users": users,
            "tickets_json": tickets_json,
            "scheduled_movie_json": scheduled_movie_json,
            "users_json": users_json
        }
        
        return context

class AdminDashboardAddTicketView(View):
    def get(self, request):
        return redirect("admin_dashboard_tickets")
        
    def post(self, request):
        add_ticket_form = AddTicketForm(request.POST)
        
        if add_ticket_form.is_valid():
            user_id = add_ticket_form.cleaned_data["user"]
            scheduled_movie_id = add_ticket_form.cleaned_data["scheduled_movie"]
            
            user_instance = get_object_or_404(CustomUser, id=user_id)
            scheduled_movie_instance = get_object_or_404(ScheduledMovie, id=scheduled_movie_id)
            
            seat_identifier = add_ticket_form.cleaned_data["seat_identifier"]
            
            if Ticket.objects.filter(scheduled_movie=scheduled_movie_instance, seat_identifier=seat_identifier, is_active=True).exists():
                messages.error(request, "This seat is already taken. Please choose another seat.")
                # context = self.init_context()
                # context["add_ticket_form"] = add_ticket_form
                # return render(request, "sections/tickets.html", context)
                return redirect("admin_dashboard_tickets")

            
            new_ticket = Ticket(
                user=user_instance,
                scheduled_movie=scheduled_movie_instance,
                seat_identifier=seat_identifier
            )
            
            new_ticket.save()
            messages.success(request, "Ticket successfully booked!")
        else:
            messages.error(request, "Failed to book a ticket. Please try again.")
            print(add_ticket_form.errors)  # Print form errors for debugging
            
            for field, errors in add_ticket_form.errors.items():
                for error in errors:    
                    messages.error(request, f"{field.capitalize()}: {error}")
        
        # return redirect("admin_dashboard_tickets")
        
        # context = self.init_context()
        # context["add_ticket_form"] = add_ticket_form
        # return render(request, "sections/tickets.html", context)
        return redirect("admin_dashboard_tickets")

    def init_context(self):
        #for displaying by scheduled_movie
        scheduled_movies = ScheduledMovie.objects.select_related("movie").prefetch_related("movie_tickets").all()
        
        #for displaying by tickets only
        tickets = Ticket.objects.select_related("user", "scheduled_movie__movie", "scheduled_movie__cinema").all()
        for ticket in tickets:
            ticket.available_seats = ticket.scheduled_movie.cinema.capacity - ticket.scheduled_movie.audience_number
        
        #for displaying by users
        users = CustomUser.objects.prefetch_related("user_tickets").all()
        
        context = {
            "scheduled_movies": scheduled_movies,
            "tickets": tickets,
            "users": users
        }
        
        return context

class AdminDashboardCancelTicketView(View):
    def get(self, request, ticket_id):
        return HttpResponseForbidden("GET requests are forbidden")
    
    def post(self, request, ticket_id):
        ticket_instance = get_object_or_404(Ticket, id=ticket_id)
        ticket_instance.is_active = False
        ticket_instance.save()
        messages.success(request, "Ticket successfully cancelled. Seat can now be booked.")
        return redirect("admin_dashboard_tickets")

class AdminDashboardCinema(View):
    
    def get(self, request):
        add_cinema_form = AddCinemaForm()
        
        context = {
            "add_cinema_form": add_cinema_form,
        }

        return render(request, "sections/cinema.html", context)
        
class AdminDashboardAddCinema(View):
    def post(self, request):
        add_cinema_form = AddCinemaForm(request.POST)
        if add_cinema_form.is_valid():
            capacity = add_cinema_form.cleaned_data.get("capacity")
            cinema_name = add_cinema_form.cleaned_data.get("cinema_name")
             
            new_cinema = Cinema(
                capacity=capacity,
                cinema_name=cinema_name
            )
            
            new_cinema.save()
            messages.success(request, "A new cinema has been created!")
            return redirect("admin_dashboard_cinema")
        else:
            messages.error(request, "Failed to create a new cinema")
            print(add_cinema_form.errors)  # Print form errors for debugging
        
          
        context = {
            "add_cinema_form": add_cinema_form
        }
        
        return render(request, "sections/cinema.html", context)

class AdminDashboardAddScheduledMovieView(View):
    def get(self, request):
        scheduled_movie_form = AddScheduledMovieForm()
        movies = self.get_movies()
        
        context = {
            "scheduled_movie_form": scheduled_movie_form,
            "movies": movies
        }
        
        return render(request, "sections/scheduled_movies.html", context)

    def post(self, request):
        scheduled_movies = self.get_movies()
        scheduled_movie_form = AddScheduledMovieForm(request.POST)
        if scheduled_movie_form.is_valid():
            movie_id = scheduled_movie_form.cleaned_data.get("movie")
            movie_instance = get_object_or_404(Movie, id=movie_id)
            cinema_id = scheduled_movie_form.cleaned_data.get("cinema")
            cinema_instance = get_object_or_404(Cinema, id=cinema_id)
            schedule = scheduled_movie_form.cleaned_data.get("schedule")
            audience_number = scheduled_movie_form.cleaned_data.get("audience_number")
            
            scheduled_movie = ScheduledMovie(
                movie=movie_instance,
                cinema=cinema_instance,
                schedule=schedule,
                audience_number=audience_number
            )
            
            scheduled_movie.save()
            messages.success(request, "A new scheduled movie has been successfully added!")
            return redirect("admin_dashboard_add_scheduled_movie")
        else:
            messages.error(request, "Failed to add a new scheduled movie")
            print(scheduled_movies_form.errors)  # Print form errors for debugging
            
        context = {
            "scheduled_movie_form": scheduled_movie,
            "scheduled_movies": scheduled_movies
        }
        
               
        return render(request, "sections/scheduled_movies.html", context)
        

    def get_movies(self):
        movies = Movie.objects.all()
        return movies