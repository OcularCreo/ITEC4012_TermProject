from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login_user(request):

    if request.method == "POST":
        username = request.POST['username-input']
        password = request.POST['password-input']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, ("login sucessful"))
            return redirect('home')
        else:
            #messages.success(request, ("Incorrect login"))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out"))
    return redirect('home')