from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Customer
from django.views.decorators.cache import never_cache

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username has already been taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                userLogin = auth.authenticate(username=username, password=password)
                auth.login(request, userLogin)

                userModel = User.objects.get(username=username)
                newCustomer = Customer.objects.create(user=userModel)
                newCustomer.save()
                return redirect('home')
        
        else:
            messages.info(request, 'Password do not match')
            return redirect('register')

    context = {}
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Account does not exist')
            return redirect('login')
        
    return render(request, 'login.html')

@login_required(login_url='login')
def profile(request, username):
    userObject = User.objects.get(username=username)
    customer = Customer.objects.get(user=userObject)
    context = {"customer": customer,}

    return render(request, 'profile.html', context)


def home(request):
    return render(request, 'index.html')