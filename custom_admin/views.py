from django.shortcuts import render
from django.views import View
from .forms import AdminLoginForm, AddMovieForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

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
                    return render(request, "pages/dashboard.html")
                else:
                    form.add_error(None, "User must be an admin to access this page")
            else:
                form.add_error("password", "Incorrect password")
        else:
            print(form.errors)
            
        return render(request, "pages/login.html", {"form": form})

class AdminDashboardView(LoginRequiredMixin, View):
    login_url = "/admin/login/"  # Specify the login URL here
    redirect_field_name = "next"  # This is the default field to redirect after login

    def get(self, request):
        return render(request, "pages/dashboard.html")

class AdminAddMovieView(View):
    def get(self, request):
        form = AddMovieForm()
        return render(request, "sections/add_movie.html", {"form": form})
    
    def post(self, request):
        form = AddMovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard_add_movie")

        return render(request, "sections/add_movie.html", {"form": form})
        