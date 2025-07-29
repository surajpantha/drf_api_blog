
from django.urls import path
from . import views
from .views import create_admin_user


urlpatterns = [
    path('register_user/', views.register_user,name='register_user'),
    path("create_blog/", views.create_blog, name="create_blog"),
    path("blog_list/", views.blog_list, name="blog_list"),
    path("update_blog/<int:pk>/", views.update_blog, name="update_blog"),
    path("delete_blog/<int:pk>/", views.delete_blog,name="delete_blog"),
    path("update_userprofile/", views.update_userprofile,name="update_userprofile"),
     path("create-admin/", create_admin_user),

]


