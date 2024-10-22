from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from core.models import User
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.core.files.storage import default_storage
import re, os

@never_cache
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            if len(password) < 1:
                messages.info(request, 'Password must be at least 1 characters long')
                return redirect('register')

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username has already been taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                userLogin = auth.authenticate(username=username, password=password)
                auth.login(request, userLogin)

                userModel = User.objects.get(username=username)
                # newCustomer = Customer.objects.create(user=userModel)
                # newCustomer.save()
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
            messages.info(request, 'Invalid username or password')
            return redirect('login')
        
    return render(request, 'login.html')

@login_required(login_url='login')
def profile(request):
    userObject = request.user
    # customer = Customer.objects.get(user=userObject)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')
        address = request.POST.get('address')
        userImage = request.FILES.get('imageInput')

        # Full name
        if full_name != '':
            nameParts = full_name.split(" ")
            userObject.first_name = nameParts[0]
            userObject.last_name = ' '.join(nameParts[1:]) if len(nameParts) > 1 else ''
        elif not userObject.first_name and not userObject.last_name:
            messages.info(request, "Enter your full name")
            return redirect('profile')
        
        # Email
        if email != '' and email != 'None':
            if re.match(r'^[\w\.-]+@gmail\.com$', email):
                userObject.email = email
            else:
                messages.info(request, "Invalid email format. Enter a valid @gmail.com email")
                return redirect('profile')
        elif not userObject.email:
            messages.info(request, "Enter your email")
            return redirect('profile')
        else:
            userObject.email = email

        # Phone
        if phone != '' and phone != 'None':
            userObject.phone = phone
        elif not userObject.phone:
            messages.info(request, 'Enter your phone number')
            return redirect('profile')

        # Gender   
        userObject.gender = gender

        # Date of birth
        try:
            userObject.dateOfBirth = datetime.strptime(f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}', "%Y-%m-%d")
        except ValueError:
            messages.info(request, "Invalid date of birth")
            return redirect('profile')

        # Address
        if address and address != 'None':
            userObject.address = address
        elif not userObject.address:
            messages.info(request, 'Enter your address')
            return redirect('profile', username=userObject.username)

        if userImage:
            oldImagePath = userObject.userImage.path if userObject.userImage else None
            userObject.userImage = userImage
            if oldImagePath and default_storage.exists(oldImagePath):
                default_storage.delete(oldImagePath)

        userObject.save()
        # customer.save()
        return redirect('profile')
    context = {"user": userObject,}

    return render(request, 'profile.html', context)

@login_required(login_url='login')
@never_cache
def logout(request):
    auth.logout(request)
    return redirect('home')




def home(request):
    return render(request, 'index.html')