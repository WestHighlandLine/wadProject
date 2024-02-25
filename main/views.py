from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.forms import UserForm, UserProfileForm


def index(request):
    return HttpResponse("Index page")


def about(request):
    return HttpResponse("About page")


def contact_us(request):
    return HttpResponse("Contact page")


@login_required
def view_post(request): # will also need to take in an ID_slug
    return HttpResponse("View a post")


@login_required
def report_post(request): # will also need to take in an ID_slug
    return HttpResponse("report post")


def signup(request):
    return HttpResponse("Sign up page")


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
    return HttpResponse("My Account page")


#@login_required
def my_posts(request):
    return HttpResponse("My Posts page")


@login_required
def edit_post(request): # needs a slug for post ID
    return HttpResponse("Edit page")


@login_required
def create_post(request):
    return HttpResponse("Create Post page")


# will also need a cookie handler if we need cookies.
    

