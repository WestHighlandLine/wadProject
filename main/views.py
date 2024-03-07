from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from main.forms import UserForm, UserProfileForm, CustomPasswordChangeForm, ChangeInfoForm
from django.contrib import messages
from main.models import UserProfile, Post

def index(request):
    return render(request, 'photoGraph/index.html')


def about(request):
    return render(request, 'photoGraph/about.html')


def contact_us(request):
    return render(request, 'photoGraph/contact_us.html')


@login_required
def view_post(request, postSlug): # will also need to take in an ID_slug
    post = Post.objects.get(slug=postSlug)  
    return render(request, 'photoGraph/post.html', {'post':post})

@login_required
def report_post(request): # will also need to take in an ID_slug
    return render(request, 'photoGraph/report_post.html')


def signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

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



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('main:index'))
                # ^ could make this redirect to wherever user was looking to go to instead of just homepage.
            else:
                return HttpResponse("Your photoGraph account is disabled.")
        
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'photoGraph/login.html')



@login_required
def logout_page(request):
    logout(request)
    return redirect(reverse('main:index'))

    
    
def update_profile(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form.PasswordResetForm(request.POST)
        form.save(commit = True)



def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save
            update_session_auth_hash(request, user)
            messages.sucess(request, "Password Changed Sucessfully")
            return redirect(reverse('photoGraph:my_account')) # should go back to the my account page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'photoGraph/passwordChange.html', {'form': form})



def info_change_view(request):
    if request.method == 'POST':
        form = ChangeInfoForm(request.user, request.POST)
        if form.is_valid():
            user = form.save
            update_session_auth_hash(request, user)
            messages.sucess(request, "Information Changed Sucessfully")
            return redirect(reverse('main:my_account')) # should go back to the my account page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangeInfoForm(request.user)
    return render(request, 'photoGraph/infoChange.html', {'form': form})



@login_required
def my_account(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_posts = Post.objects.filter(user=request.user.userprofile)
        return render(request, 'photoGraph/my_account.html', {"user_profile": user_profile,"posts":user_posts})
    else:
        return redirect(reverse('main:login'))
 
      
@login_required
def report_user(request):
    return render(request, 'photoGraph/report_user.html')


@login_required
def edit_post(request,postSlug): # needs a slug for post ID
    post = Post.objects.get(slug=postSlug)  
    return render(request, 'photoGraph/edit_post.html',{'post':post})
   
   
@login_required
def create_post(request):
    return render(request, 'photoGraph/create_post.html')


POST_FILTER_ON = True
def get_posts_json(request):
    result = {}

    postObjects = []
    # Find bounds
    if POST_FILTER_ON:
        southEast = (float(request.GET.get("seLat")), float(request.GET.get("seLon")))
        northWest = (float(request.GET.get("nwLat")), float(request.GET.get("nwLon")))

        postObjects = Post.objects.filter(
            latitude__gte=southEast[0], 
            latitude__lte=northWest[0],
            longitude__gte=northWest[1],
            longitude__lte=southEast[1]
        ).order_by("-likes")
    else:
        postObjects = Post.objects.all().order_by("-likes")

    # Filter posts
    for post in postObjects:

        postDict = {
                "lat": post.latitude,
                "lon": post.longitude,
                "user_name": post.user.username_slug,
                "location_name": post.locationName,
                "likes": post.likes,
                "date": post.aboutTime,
                "caption": post.caption,
                "photo_url": post.photo.url
            }
        if (post.locationName not in result.keys()):
            result[post.locationName] = [postDict]
        else:
            result[post.locationName].append(postDict)

    return JsonResponse(result, safe=False)