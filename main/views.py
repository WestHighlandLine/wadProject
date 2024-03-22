from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
)
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from main.forms import (
    UserForm,
    UserProfileForm,
    PostForm,
    ReportForm,
    UserReportForm,
    CommentForm,
    GroupForm,
    ContactUsForm,
)
from django.contrib import messages
from main.models import UserProfile, Post, Comment, PostReport, User, UserReport, Like, Group
from django.views import View
from django.db.models import Count


def index(request):
    return render(request, "photoGraph/index.html")


def about(request):
    return render(request, "photoGraph/about.html")


def show_user_profile(request, user_profile_slug):
    context_dict = {}

    try:
        user_profile = UserProfile.objects.get(slug=user_profile_slug)
    except UserProfile.DoesNotExist:
        context_dict["user_profile"] = None
    else:
        if request.user == user_profile.user:
            return redirect(reverse("main:my_account"))

        context_dict["user_profile"] = user_profile
        context_dict["posts"] = user_profile.posts.all()

    return render(request, "photoGraph/user_profile.html", context=context_dict)


def show_location(request):
    location_name = request.GET.get("location_name", "")
    context_dict = {"location_name": location_name}

    try:
        location_posts = Post.objects.filter(location_name=location_name)
        context_dict["posts"] = location_posts

    except Exception:
        pass

    return render(request, "photoGraph/location.html", context=context_dict)


def view_post(request, user_profile_slug, post_slug):
    context_dict = {}

    context_dict["comment_form"] = CommentForm()

    try:
        post = Post.objects.get(slug=post_slug)
        context_dict["post"] = post
        context_dict["comments"] = post.comments.all()

        if request.user.is_authenticated:
            has_user_liked = len(Like.objects.filter(post=post, user=request.user.created_by)) > 0
        else:
            has_user_liked = False

        context_dict["has_user_liked"] = has_user_liked
    except (UserProfile.DoesNotExist, Post.DoesNotExist):
        context_dict["post"] = None

    return render(request, "photoGraph/post.html", context=context_dict)


@login_required
def comment(request, post_slug):
    current_user_profile = request.user.created_by
    post = Post.objects.get(slug=post_slug)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=Comment(created_by=current_user_profile, post=post))
        form.save()

    return redirect("main:view_post", post.created_by, post_slug)


def show_group(request, group_slug):
    context_dict = {}

    try:
        group = Group.objects.get(slug=group_slug)
    except Group.DoesNotExist:
        context_dict["group"] = None
        context_dict["group_slug"] = group_slug
    else:
        context_dict["posts"] = group.posts.all()
        context_dict["group"] = group
        if request.user.is_authenticated:
            # context_dict["is_user_member"] = request.user.created_by.groups_members.filter(slug=group_slug).exists()
            context_dict["is_user_member"] = group.members.filter(id=request.user.created_by.id).exists()
            context_dict["user_is_creator"] = request.user.created_by.id == group.created_by.id
        else:
            context_dict["is_user_member"] = False
            context_dict["user_is_creator"] = False
        context_dict["posts"] = group.posts.all()

    return render(request, "photoGraph/group.html", context=context_dict)


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user.created_by
            group.save()

            return redirect(reverse("main:show_group_list"))
        else:
            print(form.errors)
            messages.error(request, "Please correct the error below.")
    else:
        form = GroupForm()
    return render(request, "photoGraph/create_group.html", {"form": form})


def join_group(request):
    if request.user.is_authenticated:
        group_slug = request.GET["group_slug"]
        try:
            group = Group.objects.get(slug=group_slug)
        except Group.DoesNotExist:
            return HttpResponseNotFound()
        except ValueError:
            return HttpResponseBadRequest()

        user_profile = request.user.created_by
        user_in_group = user_profile.groups_members.filter(slug=group_slug).exists()

        if user_in_group:
            user_profile.groups_members.remove(group)
        else:
            user_profile.groups_members.add(group)

    return JsonResponse({"user_in_group": not user_in_group, "group_size": group.members.count()}, safe=False)


def show_group_list(request):
    context_dict = {}
    context_dict["groups"] = sorted(Group.objects.all(), key=lambda x: x.members.all().count(), reverse=True)
    return render(request, "photoGraph/group_list.html", context=context_dict)


@login_required
def report_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)

    if request.method == "POST":
        form = ReportForm(
            request.POST,
            instance=PostReport(reporter=request.user.created_by, post_id=post),
        )
        if form.is_valid():
            form.save()
            return render(
                request,
                "photoGraph/report_post.html",
                {"post": post, "form": form, "show_popup": True},
            )
    else:
        form = ReportForm()
    return render(request, "photoGraph/report_post.html", {"post": post, "form": form})


@login_required
def report_detail(request, report_id):
    if not request.user.is_superuser:
        return redirect("main:index")

    report = get_object_or_404(PostReport, id=report_id)
    related_reports = PostReport.objects.filter(post_id=report.post_id).exclude(id=report_id)
    reasons = [report.reason] + list(related_reports.values_list("reason", flat=True))
    return render(request, "photoGraph/report_detail.html", {"report": report, "reasons": reasons})


@login_required
def delete_post_view(request, post_id):
    if not request.user.is_superuser:
        return redirect("main:index")

    post = get_object_or_404(Post, id=post_id)
    post_reports = PostReport.objects.filter(post_id=post.id)

    if request.method == "POST":
        post_reports.delete()
        post.delete()
        return redirect("admin:main_postreport_changelist")

    return render(request, "photoGraph/delete_post_report.html", {"post": post})


@login_required
def report_user(request, user_profile_slug):
    reported_user_profile = UserProfile.objects.get(slug=user_profile_slug)

    if request.method == "POST":
        form = UserReportForm(
            request.POST,
            instance=UserReport(reporter=request.user.created_by, user_id=reported_user_profile.user),
        )
        if form.is_valid():
            form.save()
            return render(
                request,
                "photoGraph/report_user.html",
                {"reported_user_profile": reported_user_profile, "form": form, "show_popup": True},
            )
    else:
        form = UserReportForm()
    return render(
        request,
        "photoGraph/report_user.html",
        {"reported_user_profile": reported_user_profile, "form": form},
    )


@login_required
def user_report_detail(request, report_id):
    if not request.user.is_superuser:
        return redirect("main:index")

    user_report = get_object_or_404(UserReport, id=report_id)
    related_reports = UserReport.objects.filter(user_id=user_report.user_id).exclude(id=report_id)
    reasons = [user_report.reason] + list(related_reports.values_list("reason", flat=True))

    context = {"report": user_report, "reasons": reasons}
    return render(request, "photograph/user_report_detail.html", context)


@login_required
def delete_user_view(request, user_id):
    if not request.user.is_superuser:
        return redirect("main:index")

    reported_user = get_object_or_404(User, id=user_id)
    user_reports = UserReport.objects.filter(user_id=reported_user.id)

    if request.method == "POST":
        user_reports.delete()
        reported_user.delete()
        return redirect("admin:main_userreport_changelist")

    context = {"reported_user": reported_user}
    return render(request, "photograph/delete_user_report.html", context)


def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            # Registering done! Login the user, and redirect them to where they were going
            login(request, user)
            next = request.POST.get("next", None)
            redirect_url = reverse("main:index")
            if next:
                redirect_url = next
            return redirect(redirect_url)
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "photoGraph/signup.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                next = request.POST.get("next", None)
                redirect_url = reverse("main:index")
                if next:
                    redirect_url = next
                return redirect(redirect_url)
            else:
                return HttpResponse("Your photoGraph account is disabled.")

        else:
            messages.error(request, "Invalid login details supplied. Please try again.")
            return render(request, "photoGraph/login.html", {"username": username})
    else:
        return render(request, "photoGraph/login.html")


@login_required
def logout_page(request):
    logout(request)
    return redirect(reverse("main:index"))


def update_profile(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form.PasswordResetForm(request.POST)
        form.save()


def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password Changed Sucessfully")
            return redirect("main:my_account")  # should go back to the my account page
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "photoGraph/passwordChange.html", {"form": form})


def info_change_view(request):
    user_profile = request.user.created_by

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Information Changed Sucessfully")
            return redirect(reverse("main:my_account"))  # should go back to the my account page
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "photoGraph/infoChange.html", {"form": form})


@login_required
def my_account(request):
    if request.user.is_authenticated:
        user_profile = request.user.created_by
        user_posts = user_profile.posts.all()
        return render(
            request,
            "photoGraph/my_account.html",
            {"user_profile": user_profile, "posts": user_posts},
        )
    else:
        return redirect(reverse("main:login"))


@login_required
def edit_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    return render(request, "photoGraph/edit_post.html", {"post": post})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user.created_by
            post.save()

            return redirect(reverse("main:index"))
        else:
            print(form.errors)
            messages.error(request, "Please correct the error below.")
    else:
        form = PostForm(
            request=request,
            initial={
                "latitude": request.GET.get("lat", ""),
                "longitude": request.GET.get("lng", ""),
            },
        )

    return render(request, "photoGraph/create_post.html", {"form": form})


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
            longitude__lte=southEast[1],
        )

        postObjects = sorted(postObjects, key=lambda p: len(Like.objects.filter(post=p)), reverse=True)
    else:
        postObjects = Post.objects.all()

    # Filter posts
    for post in postObjects:
        likes = Like.objects.filter(post=post)

        postDict = {
            "lat": post.latitude,
            "lon": post.longitude,
            "user_name": post.created_by.slug,
            "location_name": post.location_name,
            "location_url": reverse("main:show_location") + "?location_name=" + post.location_name,
            "likes": len(likes),
            "date": post.created_time,
            "caption": post.caption,
            "photo_url": post.photo.url,
            "user_url": reverse("main:show_user_profile", args=[post.created_by.slug]),
            "post_url": reverse("main:view_post", args=[post.created_by.slug, post.slug]),
        }
        if post.location_name not in result.keys():
            result[post.location_name] = [postDict]
        else:
            result[post.location_name].append(postDict)

    return JsonResponse(result, safe=False)


def like_toggle(request):
    if request.user.is_authenticated:
        post_id = request.GET["post_id"]
        try:
            post = Post.objects.get(id=int(post_id))
        except Post.DoesNotExist:
            return HttpResponseNotFound()
        except ValueError:
            return HttpResponseBadRequest()

        user_profile = request.user.created_by

        has_user_liked = len(Like.objects.filter(post=post, user=user_profile)) > 0

        if has_user_liked:
            # Unlike
            Like.objects.get(post=post, user=user_profile).delete()
        else:
            # Like
            Like.objects.update_or_create(post=post, user=user_profile)

    likes = Like.objects.filter(post=post)

    return HttpResponse(len(likes))


def contact_us_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has now been sent to our admin team.")
            return redirect(reverse("main:contact_us"))
    else:
        form = ContactUsForm()
    return render(request, "photoGraph/contact_us.html", {"contact_form": form})
