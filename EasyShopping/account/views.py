from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Customer
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.core.files.storage import default_storage

@never_cache
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

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        address = request.POST.get('address')
        userImage = request.FILES.get('userImage')

        try:
            userObject.first_name, userObject.last_name = full_name.split(" ", 1)
        except ValueError:
            userObject.first_name = full_name
            userObject.last_name = ''
        
        userObject.email = email
        customer.phone = phone
        customer.gender = gender
        try:
            customer.dateOfBirth = datetime.strptime(f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}', "%Y-%m-%d")
        except ValueError:
            pass

        customer.address = address
        if userImage:
            oldImagePath = customer.userImage.path if customer.userImage else None
            customer.userImage = userImage

            if oldImagePath and default_storage.exists(oldImagePath):
                default_storage.delete(oldImagePath)

        userObject.save()
        customer.save()

        return redirect('profile', username=userObject.username)

    context = {"customer": customer,}

    return render(request, 'profile.html', context)

@login_required(login_url='login')
@never_cache
def logout(request):
    auth.logout(request)
    return redirect('home')




def home(request):
    return render(request, 'index.html')