from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AdminLoginForm, AddMovieForm, AddNowShowingMovieForm, AddCinemaForm
from cinema.models import NowShowingMovie, Cinema
from movies.models import Movie
from accounts.forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

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

class AdminLogoutView(LogoutView):
    next_page = reverse_lazy("admin_login")
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Logout successful!")
        return response

class AdminDashboardMovieList(View):
    def get(self, request):
        return render(request, "sections/movie_list.html")
    
class AdminDashboardTickets(View):
    def get(self, request):
        return render(request, "sections/tickets.html")
    
class AdminDashboardCinema(View):
    def get(self, request):
        now_showing_form = AddNowShowingMovieForm()
        add_cinema_form = AddCinemaForm()
        
        context = {
            "now_showing_form": now_showing_form, 
            "add_cinema_form": add_cinema_form
        }
        
        return render(request, "sections/cinema.html", context)

class AdminDashboardAddNowShowing(View):
    def post(self, request):    
        now_showing_form = AddNowShowingMovieForm(request.POST)
        if now_showing_form.is_valid(): 
            cinema_id = now_showing_form.cleaned_data['cinema']
            cinema_instance = get_object_or_404(Cinema, id=cinema_id)
            movie_id = now_showing_form.cleaned_data['movie']
            movie_instance = get_object_or_404(Cinema, id=movie_id)
            end_date = now_showing_form.cleaned_data['end_date'] 
            
            now_showing_movie = NowShowingMovie(
                cinema=cinema_instance,  # Set the foreign key using ID
                movie=movie_instance,    # Set the foreign key using ID
                end_date=end_date    # Use the provided end date
            )
            
            now_showing_movie.save() 
            
            messages.success(request, "A new movie is now showing!")
            return redirect("admin_dashboard_cinema")
        else:
            messages.error(request, "Failed to add a new movie in Now Showing")
            print(now_showing_form.errors)  # Print form errors for debugging
        
        context = {
            "now_showing_form": now_showing_form
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
            messages.error(request, "Failed to add a new movie in Now Showing")
            print(now_showing_form.errors)  # Print form errors for debugging
        
          
        context = {
            "add_cinema_form": add_cinema_form
        }
        
        return render(request, "sections/cinema.html", context)