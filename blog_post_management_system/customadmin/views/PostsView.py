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
from django.views import View
from customadmin.mixins import HasPermissionsMixin
from django.template.loader import get_template
from django.db.models import Q
from customadmin.views.generics import MyListView


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
        print(context_data["opts"])
        context_data["count"] = self.model.objects.count()
        return context_data


################ AJAX view for post listing table #################

class UserListAjaxView(View, HasPermissionsMixin):
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
        print("Query set in prepare results : ",qs)
        for post in qs:
            print(post)
            data.append(
                {
                   "id": post.id,
                   "title":post.title,
                   "content":post.content,
                   "date_published":post.date_published,
                   "author_id":post.author_id,
                   "action":"action"
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
        
        print("#######################",queryset,"##########################")
        
        if search_value:
            queryset = queryset.filter(
                Q(title__icontains=search_value) |
                Q(content__icontains=search_value) |
                Q(date_published__icontains=search_value) |
                Q(author_id__icontains=search_value)
            )

        total_records = self.model.objects.count()
        filtered_records = queryset.count()
        queryset = queryset[start:start + length]
        data = self.prepare_results(queryset)

        context_data["data"] = data
        context_data["draw"] = draw
        context_data["recordsTotal"] = total_records
        context_data["recordsFiltered"] = filtered_records

        return JsonResponse(context_data)
    








