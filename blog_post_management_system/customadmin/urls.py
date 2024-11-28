from django.urls import path,include
from  .views.views import MyLoginView,MyUserListView
# from django.contrib.auth.templates 
urlpatterns = [
    path("login/", MyLoginView.as_view(), name="admin_login"),
    path("user/", MyUserListView.as_view(), name="user-list"),
]
