from django.shortcuts import render, HttpResponse, redirect

from cinema.models import ScheduledMovie
from sinehan.views import home_view
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import JsonResponse
# from .models import CustomUser
from django.contrib import messages

CustomUser = get_user_model()

#login_view already handles by auth.urls

#def signup_view(request):
#    return HttpResponse("signup_view")

def signup_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()  # Save the user object
            login(request, user)  # Log in the user
            return redirect('home')  # Redirect to home page
        else:
            # If the form is invalid, loop through the errors
            for field, error_list in user_form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field.capitalize()}: {error}")
                    
            # Redirect back with error messages
            return redirect('home')
    
    # For GET requests, redirect to the home page
    return redirect('home')

#Override
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # User exists and credentials are correct
            messages.success(request, 'Successfully logged in')
            login(request, user)
            return redirect('home')
        else:
            # Check if a user with the provided email exists
            if not CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Account with this email does not exist.')
            else:
                messages.error(request, 'Incorrect password.')

            return redirect('home')
        
    return render(request, 'home.html')

def logout_view(request):
    logout(request)  
    return redirect('home')


def profile_view(request):
    try:
        # user = CustomUser.objects.get(id = id)
        user = request.user
        return render(request, 'read_profile.html', {'user': user})
    except CustomUser.DoesNotExist:
        raise HttpResponse("CustomUser table not found")

def tickets_view(request):
    try:
        # user = CustomUser.objects.get(id = id)
        user = request.user
        tickets = user.user_tickets.all()
        return render(request, 'tickets.html', {'user': user, 'tickets': tickets})
    except CustomUser.DoesNotExist:
        raise HttpResponse("CustomUser table not found")

def history_view(request):
    try:
        # user = CustomUser.objects.get(id = id)
        user = request.user
        return render(request, 'history.html', {'user': user})
    except CustomUser.DoesNotExist:
        raise HttpResponse("CustomUser table not found")

def update_profile(request):
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # return redirect('profile', id=id)
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
        else:
            messages.error(request, "Erorr updating Profile Information")
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})