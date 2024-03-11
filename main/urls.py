from django.urls import path
from django.conf.urls import url
from main import views
from .views import ReportDetailView, ReportListView, DeletePostView


app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index),
    path("home", views.index),
    path("about/", views.about, name="about"),
    path("about/contact_us/", views.contact_us, name="contact_us"),
    path(
        "user/<slug:user_profile_slug>/",
        views.show_user_profile,
        name="show_user_profile",
    ),
    path(
        "location/",
        views.show_location,
        name="show_location",
    ),
    path(
        "user/<slug:user_profile_slug>/post/<slug:post_slug>",
        views.view_post,
        name="view_post",
    ),
    # ^ probably needs to be a name slug using a post ID of some sort, like category_name_slug in rango.
    # eg: path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path("report_post/", views.report_post, name="report_post"),
    # ^ will probably need to be similar to this:
    # path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),

    path('admin/report_list/', views.ReportListView, name='report_list'),
    path('admin/report_detail/<int:report_id>/', views.ReportDetailView, name='report_detail'),
    path('admin/delete_post/<int:post_id>/', views.DeletePostView, name='delete_post'),
    #path('view_post/<int:post_id>/', views.ReportPostView, name='report_post'),

    path("signup/", views.signup, name="signup"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("my_account/", views.my_account, name="my_account"),
    path("password_Change/", views.password_change_view, name="passwordChange"),
    path("infoChange/", views.info_change_view, name="infoChange"),
    path("my_posts/edit/<slug:postSlug>", views.edit_post, name="edit_post"),
    # ^ may also need a slug
    path("get_posts_json", views.get_posts_json, name="get_posts_json"),
    path("create_post/", views.create_post, name="create_post"),
    path("update_profile/", views.update_profile, name="update_profile"),
]
