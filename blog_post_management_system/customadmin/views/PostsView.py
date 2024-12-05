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
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect,JsonResponse
from django.views import View
from customadmin.mixins import HasPermissionsMixin
from django.template.loader import get_template
from django.db.models import Q
from customadmin.views.generics import MyCreateView, MyListView
from customadmin.forms.blogs_form import BlogPostForm
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from likes.models import Like
from comments.models import UserComments
from django.contrib.auth.models import User

class listBlogs(MyListView):
    """This view is used to list all the blogs"""

    model = BlogPost
    template_name = "Blogs/blog_list_admin.html"
    context_object_name = "posts"
    ordering = ["-date_published"]

    def get_queryset(self):
        """Override queryset to add extra functionality"""
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["opts"] = self.model._meta
        context_data["count"] = self.model.objects.count()
        return context_data


################ AJAX view for post listing table #################

class BlogListAjaxView(View, HasPermissionsMixin):
    """
    Ajax-Pagination view for Bloglisting
    """
    template_name = "Blogs/blog_list_admin.html"
    model = BlogPost

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def is_orderable(self):
        """Check if order is defined in dictionary."""
        return True

    def _get_actions(self, obj):
        """Get actions column markup."""
        t = get_template("partials/list_actions.html")
        opts = self.model._meta
        return t.render(
            {
                "obj": obj,
                "opts": opts,
                "has_change_permission": self.has_change_permission(self.request),
                "has_delete_permission": self.has_delete_permission(self.request),
            }
        )

    def _get_check(self, active: bool):
        template = get_template("partials/list_boolean.html")
        return template.render({"bool_val": active})

    def prepare_results(self, qs):
        """Prepare final result data here."""

        data = []
        
        for post in qs:
            print(post)
            current_user = User.objects.get(id=post.author_id)
            print("Current user : ############",current_user,post.author_id)
            
            data.append(
                {
                   "id": post.id,
                   "title":post.title,
                   "content":post.content,
                   "date_published":post.date_published,
                   "author_id":current_user.username,
                   "action":self._get_actions(post)
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = {}
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        draw = int(request.GET.get("draw", 1))
        search_value = request.GET.get("search[value]", "").strip()
        queryset = self.model.objects.all()

        # if search_value:
        #     queryset = queryset.filter(
        #         Q(title__icontains=search_value) |
        #         Q(content__icontains=search_value) |
        #         Q(date_published__icontains=search_value) |
        #         Q(author_id__icontains=search_value)
        #     )

        total_records = self.model.objects.count()
        filtered_records = queryset.count()
        queryset = queryset[start:start + length]
        data = self.prepare_results(queryset)

        context_data["data"] = data
        context_data["draw"] = draw
        context_data["recordsTotal"] = total_records
        context_data["recordsFiltered"] = filtered_records

        return JsonResponse(context_data)
    

class UpdatePostView(UpdateView,View):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'Blogs/blog_update_admin.html'
    success_url = reverse_lazy('admin_post:list-post-admin') 


class CreateBlogView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "Blogs/blog_create_admin.html"
    success_url = reverse_lazy('admin_post:list-post-admin') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteBlogView(DeleteView):
    """This view is used to delete existing blog"""

    def get(self, request, pk):
        try:
            current_blog = BlogPost.objects.get(id=pk)
            current_blog.delete()
            messages.success(self.request, f"Blog deleted.")
            return HttpResponseRedirect(reverse("admin_post:list-post-admin"))
        except current_blog.DoesNotExist:
            return HttpResponse("Given post does not exist!")


class BlogDetailView(DetailView):
    """This view is used to show selected blog"""

    template_name = "Blogs/blog_detail_admin.html"
    model = BlogPost
    fields = ['id','title','content', 'author', 'date_published','likes_count']

    def get_object(self):
        blog_post = super().get_object()
        return blog_post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_post = self.get_object()
        likes = Like.objects.filter(post_id=blog_post).count()

        context['likes'] = likes
        context['blog_id'] = blog_post.id
        comments = UserComments.objects.filter(post_id=blog_post)
        context['comments'] = comments
        return context

    def get(self, request, pk, *args, **kwargs):
        return super().get(request, pk, *args, **kwargs)


class DeleteCommentView(DeleteView):
    """This view is used to delete existing comments"""
    model = UserComments

    def get_success_url(self):
        """Redirect to the blog post detail page after successful deletion"""
        return reverse("admin_post:blogpost-detail", kwargs={"pk": self.object.post_id_id})
    
    def get(self, request, pk):
        try:
            current_comment = self.model.objects.get(id=pk)
            current_comment.delete()
            messages.success(self.request, f"Comment deleted.")
            return HttpResponseRedirect(reverse("admin_post:blogpost-detail"), kwargs={"pk": current_comment.post_id})
        except current_comment.DoesNotExist:
            return HttpResponse("Given comment does not exist!")
        
class CreateCommentView(CreateView):
    
    model = BlogPost

    def form_valid(self, form):
        form.instance.post_id = BlogPost.objects.get(pk=self.kwargs["blog_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_comment", kwargs={"pk": self.kwargs["pk"]})
    
    def get(self, request, pk):
        try:
            current_comment = UserComments.objects.get(id=pk)
            current_comment.delete()
            messages.success(self.request, f"Comment deleted.")
            return HttpResponseRedirect(reverse("admin_post:blogpost-detail"), kwargs={"pk": current_comment.post_id})
        except current_comment.DoesNotExist:
            return HttpResponse("Given comment does not exist!")

        




    



