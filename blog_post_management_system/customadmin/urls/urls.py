from django.urls import path,include
from  ..views.views import MyLoginView,MyUserListView,UserListAjaxView,CreateUserView,UpdateUserView,MyUserDeleteView,UserProfileView,LogoutView
# from django.contrib.auth.templates 

# app_name = "user"

urlpatterns = [
    path("",include('customadmin.urls.account_urls')),
    path("posts/",include('customadmin.urls.posts_urls')),

    # path("", MyLoginView.as_view(), name="admin_login"),
    # path("user/", MyUserListView.as_view(), name="user-list"),
    # path("logout",LogoutView.as_view(),name="logout"),
    # path("user-list-ajax/", UserListAjaxView.as_view(), name="user-list-ajax"),
    # path("user/create", CreateUserView.as_view(), name="user-create"),
    # path("user/<pk>/", UserProfileView.as_view(), name="profile"),
    # path("user/<pk>/update/", UpdateUserView.as_view(), name="user-update"),
    # path("user-delete/<pk>/", MyUserDeleteView.as_view(), name="user-delete"),
    
]
