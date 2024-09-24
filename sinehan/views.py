from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def movies_view(request):
    return render(request, 'movies.html')

def home_view(request):
    return render(request, 'home.html')