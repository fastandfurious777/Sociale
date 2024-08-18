from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout 

from . forms import CreateUserForm,LoginUserForm

def home(request):
    #Dummy data
    context = {
        'available_bikes': 20,
        'active_users': User.objects.filter(is_active=True).count(),
        'dollars_saved': 5000
    }
    return render(request, 'base/index.html', context)

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'base/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            #Authentication has been handled by the form
            user = form.get_user()  
            if user is not None:
                login(request, user)  
                return redirect('map-home')  
    else:
        form = LoginUserForm()
    return render(request, 'base/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')