from django.urls import path
from django.conf.urls import url
from main import views


app_name = 'photoGraph'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('about/contact_us/', views.contact_us, name='contact_us'),
    path('view_post/', views.view_post, name='view_post'), 
    # ^ probably needs to be a name slug using a post ID of some sort, like category_name_slug in rango.
    # eg: path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),

    path('report_post/', views.report_post, name='report_post'),
    # ^ will probably need to be similar to this:
    # path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my_account/', views.my_account, name='my_account'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('my_posts/edit/', views.edit_post, name='edit_post'),
    # ^ may also need a slug

    path('create_post/', views.create_post, name='create_post'),
]