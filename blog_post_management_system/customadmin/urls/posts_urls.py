from django.urls import path,include
from customadmin.views.PostsView import listBlogs,BlogListAjaxView,UpdatePostView,CreateBlogView,DeleteBlogView,BlogDetailView,DeleteCommentView,CreateCommentView
# from django.contrib.auth.templates 

app_name = "admin_post"

urlpatterns = [
    path("",listBlogs.as_view(),name='list-post-admin'),
    path("post/",BlogListAjaxView.as_view(),name='list-post-ajax-view'),
    path("update/<pk>",UpdatePostView.as_view(),name='blogpost-update'),
    path("create/",CreateBlogView.as_view(),name='blogpost-create'),
    path("delete/<pk>",DeleteBlogView.as_view(),name='blogpost-delete'),
    path("<pk>/",BlogDetailView.as_view(),name = "blogpost-detail"),
    path("delete_comment/<pk>",DeleteCommentView.as_view(),name = "comment-delete"),
    path("create_comment/<blog_id>",CreateCommentView.as_view(),name = "comment-create"),
]
