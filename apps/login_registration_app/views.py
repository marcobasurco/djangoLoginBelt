from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages, sessions
from .models import User
from datetime import datetime
import bcrypt

def index(request):

    return render(request, 'login_registration_app/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['email'] = request.POST['email']
    request.session['birthdate'] = request.POST['birthdate']
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode('utf8'), bcrypt.gensalt())
        newUser = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        birthdate=request.POST['birthdate'],
        password=hash1.decode('utf8'))
    return redirect('/success')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/')

    emailCheck = User.objects.filter(email=request.POST['email'])
    loginUser = emailCheck[0]
    newDate = datetime.strftime(loginUser.birthdate, "%Y-%m-%d")

    if bcrypt.checkpw(request.POST['password'].encode('utf8'), loginUser.password.encode('utf8')):
        request.session['userId'] = loginUser.id
        request.session['firstName'] = loginUser.first_name
    if newDate == request.POST['birthdate']:
        return redirect('/success')
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def success(request):
    if "userId" not in request.session:
        return redirect('/')
    return render(request, 'login_registration_app/success.html')


def wall(request):
    if "userId" not in request.session:
        return redirect('/')
    return render(request, 'login_registration_app/wall.html')
