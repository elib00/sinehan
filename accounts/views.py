from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import JsonResponse
# from .models import CustomUser

CustomUser = get_user_model()

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
            #TODO create 404 not found page
            return render(request, 'hello.html', {'error': 'Invalid credentials'})
        
    #TODO: Fix login required in movies_view
    return render(request, 'home.html')

def logout_view(request):
    logout(request)  
    return redirect('home')


def profile_view(request, id):
    try:
        user = CustomUser.objects.get(id = id)
        return render(request, 'read_profile.html', {'user': user})
    except CustomUser.DoesNotExist:
        raise HttpResponse("CustomUser table not found")

def tickets_view(request, id):
    try:
        # user = CustomUser.objects.get(id = id)
        tickets = user.user_tickets.all()
        return render(request, 'tickets.html', {'user': request.user})
    except CustomUser.DoesNotExist:
        raise HttpResponse("CustomUser table not found")

def history_view(request, id):
    try:
        user = CustomUser.objects.get(id = id)
        return render(request, 'history.html', {'user': user})
    except CustomUser.DoesNotExist:
        raise HttpResponse("CustomUser table not found")

def update_profile(request, id):
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=id)
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})