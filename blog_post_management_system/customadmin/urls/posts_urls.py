from django.urls import path,include
from customadmin.views.PostsView import listBlogs
# from django.contrib.auth.templates 

app_name = "admin_post"

urlpatterns = [
    path("",listBlogs.as_view(),name='list-post-admin'),
]
