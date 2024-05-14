from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from users.forms import UserRegistrationForm
from django_blog import settings

def register(request):
    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            auth.login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        register_form = UserRegistrationForm()
    context = {
        'register_form' : register_form
    }
    return render(request, 'register.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.warning(request, "Invalid username/password!")
    return render(request, 'login.html', {})
  
def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')
