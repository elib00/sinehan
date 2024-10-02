from django.shortcuts import render
from django.views import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.
class AdminLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)  
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_superuser and user.is_staff:
                    login(request, user)
                    return render(request, "login.html", {"form": form})
                else:
                    form.add_error(None, "User must be an admin to access this page")
            else:
                form.add_error("password", "Incorrect password")
        else:
            print(form.errors)
            
        return render(request, "login.html", {"form": form})