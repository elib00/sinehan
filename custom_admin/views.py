from django.shortcuts import render, redirect
from django.views import View
from .forms import AdminLoginForm, AddMovieForm
from accounts.forms import CustomUserCreationForm
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
                    return redirect(reverse('admin_dashboard'))
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

class AdminDashboardAllUsersView(View):
    def get(self, request):
        form = AddMovieForm()
        users = CustomUser.objects.all()
        return render(request, "sections/all_users.html", {"users": users, "add_movie_form": form})

class AdminLogoutView(LogoutView):
    next_page = reverse_lazy("admin_login")
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Logout successful!")
        return response
