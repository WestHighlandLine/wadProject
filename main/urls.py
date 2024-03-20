from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index),
    path("home/", views.index),
    path("about/", views.about, name="about"),
    path("user/<slug:user_profile_slug>/", views.show_user_profile, name="show_user_profile"),
    path("location/", views.show_location, name="show_location"),
    path("user/<slug:user_profile_slug>/post/<slug:post_slug>/", views.view_post, name="view_post"),
    path("report_post/<slug:post_slug>/", views.report_post, name="report_post"),
    path("admin/report_detail/<int:report_id>/", views.report_detail, name="report_detail"),
    path("admin/delete_post_view/<int:post_id>/", views.delete_post_view, name="delete_post_view"),
    path("report_user/<slug:user_profile_slug>/", views.report_user, name="report_user"),
    path("admin/user_report_detail/<int:report_id>/", views.user_report_detail, name="user_report_detail"),
    path("admin/delete_user_view/<int:user_id>/", views.delete_user_view, name="delete_user_view"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("my_account/", views.my_account, name="my_account"),
    path("password_Change/", views.password_change_view, name="passwordChange"),
    path("info_change/", views.info_change_view, name="info_change"),
    path("my_posts/edit/<slug:post_slug>/", views.edit_post, name="edit_post"),
    path("get_posts_json", views.get_posts_json, name="get_posts_json"),
    path("create_post/", views.create_post, name="create_post"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("like_toggle/", views.like_toggle, name="like_toggle"),
    path("group/<slug:group_slug>/", views.show_group, name="show_group"),
    path("group_list/", views.show_group_list, name="show_group_list"),
    path("create_group/", views.create_group, name="create_group"),
    path("join_group/", views.join_group, name="join_group"),
    path("contact/", views.contact_us_view, name="contact_us"),
    path("comment/<slug:post_slug>/", views.comment, name="comment"),
]
