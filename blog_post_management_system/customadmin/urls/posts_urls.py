from django.urls import path,include
from customadmin.views.PostsView import listBlogs
# from django.contrib.auth.templates 

urlpatterns = [
    path("",listBlogs().as_view(),name='list-post-admin')
]
