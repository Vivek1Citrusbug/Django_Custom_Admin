from django.urls import path,include
from  .views.views import MyLoginView,MyUserListView,UserListAjaxView,CreateUserView,UpdateUserView,MyUserDeleteView,UserProfileView
# from django.contrib.auth.templates 
app_name = "user"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="admin_login"),
    path("user/", MyUserListView.as_view(), name="user-list"),
    path("user-list-ajax/", UserListAjaxView.as_view(), name="user-list-ajax"),
    path("user/create", CreateUserView.as_view(), name="user-create"),
    path("user/<pk>/", UserProfileView.as_view(), name="profile"),
    path("user/<pk>/update/", UpdateUserView.as_view(), name="user-update"),
    path("user-delete/<pk>/", MyUserDeleteView.as_view(), name="user-delete"),
]
