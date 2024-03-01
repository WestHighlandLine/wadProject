from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from main.forms import UserForm, UserProfileForm
from django.contrib import messages
from main.models import UserProfile, Post

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
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'photoGraph/signup.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})


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

    
    
def update_profile(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form.PasswordResetForm(request.POST)
        form.save(commit = True)

def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save
            update_session_auth_hash(request, user)
            messages.sucess(request, "Password Changed Sucessfully")
            return redirect(reverse('photoGraph:my_account')) # should go back to the my account page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'photoGraph/passwordChange.html', {'form': form})

#@login_required
def my_account(request):
    #if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        return render(request, 'photoGraph/my_account.html', {'user_profile': user_profile})
 
      



@login_required
def edit_post(request): # needs a slug for post ID
    return render(request, 'photoGraph/edit_post.html')


@login_required
def create_post(request):
    return render(request, 'photoGraph/create_post.html')


# will also need a cookie handler if we need cookies.
    

def get_posts_json(request):
    result = []
    for post in Post.objects.all():
        result.append({
            "lat": post.latitude,
            "lon": post.longitude,
            "caption": post.caption,
            "photo_url": post.photo.url
        })
    return JsonResponse(result, safe=False)