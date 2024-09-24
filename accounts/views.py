from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse


#login_view already handles by auth.urls

#def signup_view(request):
#    return HttpResponse("signup_view")

def signup_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
    
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('home')
    
    else:
        user_form = CustomUserCreationForm()


#Override
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'hello.html', {'error': 'Invalid credentials'})
        
    #TODO: Fix login required in movies_view
    return render(request, 'home.html')

def logout_view(request):
    logout(request)  
    return redirect('home')
