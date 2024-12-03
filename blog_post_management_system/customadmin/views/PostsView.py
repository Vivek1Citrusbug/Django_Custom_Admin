from blogs.models import BlogPost
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from customadmin.forms.blogs_form import BlogPostForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

class listBlogs(LoginRequiredMixin,ListView):
    """This view is used to list all the blogs"""

    model = BlogPost
    template_name = "blogs/blog_list.html"
    context_object_name = "posts"
    ordering = ["-date_published"]

    def blog_list_ajax(request):
    









# class BlogDetailView(LoginRequiredMixin, DetailView):
#     """This view is used to give detail of selected blog"""

#     model = BlogPost
#     template_name = "blogs/blog_detail.html"
#     context_object_name = "post"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         context["likes_count"] = post.likes.count()
#         context["user_liked"] = post.likes.filter(
#             user=self.request.user
#         ).exists()  
#         return context


# class BlogCreateView(LoginRequiredMixin, CreateView):
#     """This view is used to create new blog"""

#     model = BlogPost
#     form_class = BlogPostForm
#     template_name = "blogs/blog_form.html"
#     success_url = reverse_lazy("list-post-admin")

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     """This view is used to update existing blog"""

#     model = BlogPost
#     form_class = BlogPostForm
#     template_name = "blogs/blog_form.html"
#     success_url = reverse_lazy("list-post-admin")

#     def test_func(self):
#         post = self.get_object()
#         return post.author == self.request.user


# class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     """This view is used to delete existing blog"""

#     model = BlogPost
#     template_name = "blogs/blog_confirm_delete.html"
#     success_url = reverse_lazy("list-post-admin")
#     context_object_name = "post"

#     def test_func(self):
#         post = self.get_object()
#         return post.author == self.request.user or self.request.user.is_staff
