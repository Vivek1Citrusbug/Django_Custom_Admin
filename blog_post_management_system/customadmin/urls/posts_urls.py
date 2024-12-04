from django.urls import path,include
from customadmin.views.PostsView import listBlogs,UserListAjaxView
# from django.contrib.auth.templates 

app_name = "admin_post"

urlpatterns = [
    path("",listBlogs.as_view(),name='list-post-admin'),
    path("",UserListAjaxView.as_view(),name ='list-post-ajax-view')
]
