from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.forms import UserForm, UserProfileForm


def index(request):
    return render(request, 'photoGraph/index.html')


def about(request):
    return render(request, 'photoGraph/about.html')


def contact_us(request):
    return render(request, 'photoGraph/contact_us.html')


@login_required
def view_post(request): # will also need to take in an ID_slug
    return render(request, 'photoGraph/post.html')


@login_required
def report_post(request): # will also need to take in an ID_slug
    return render(request, 'photoGraph/report_post.html')


def signup(request):
    return render(request, 'photoGraph/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('photoGraph:index'))
                # ^ could make this redirect to wherever user was looking to go to instead of just homepage.
            else:
                return HttpResponse("Your photoGraph account is disabled.")
        
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'photoGraph/login.html')


@login_required
def logout(request):
    logout(request)
    return redirect(reverse('photoGraph:index'))


#login_required
def my_account(request):
    return render(request, 'photoGraph/my_account.html')


@login_required
def edit_post(request): # needs a slug for post ID
    return render(request, 'photoGraph/edit_post.html')


@login_required
def create_post(request):
    return render(request, 'photoGraph/create_post.html')


# will also need a cookie handler if we need cookies.
    

