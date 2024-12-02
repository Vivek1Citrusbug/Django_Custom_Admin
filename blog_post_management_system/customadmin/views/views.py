from datetime import timezone
import re
from typing import Dict
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.urls import reverse
from blog_post_management_system import settings
from customadmin.forms.users import LoginForm,CreateUserForm,UpdateUserForm,AuthenticationForm
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import get_permission_codename
from customadmin.mixins import ModelOptsMixin,HasPermissionsMixin
from django.template.loader import get_template
from django.db.models import Q
from customadmin.views.generics import MyCreateView,MyUpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class MyLoginRequiredMixins(LoginRequiredMixin):
    """
    Custom Login Required Mixins that override the handle_no_permission method
    """

    def handle_no_permission(self) -> HttpResponseRedirect:
        """Redirect to the admin login page"""
        if self.request.user.is_authenticated:
            return render(
                self.request,
                "403.html",
                status=403,
            )
        return redirect("user:admin_login")
    

class MyPermissionRequiredMixin(PermissionRequiredMixin):
    raise_exception = True

    def get_permission_required(self):
        """Default to view and change perms."""
        opts = self.model._meta
        codename_view = get_permission_codename("view", opts)
        codename_change = get_permission_codename("change", opts)
        view_perm = f"{opts.app_label}.{codename_view}"
        change_perm = f"{opts.app_label}.{codename_change}"
        perms = (view_perm, change_perm)
        return perms


class MyListView(MyLoginRequiredMixins,MyPermissionRequiredMixin,ModelOptsMixin,HasPermissionsMixin,ListView):
    """ListView CBV with LoginRequiredMixin and PermissionRequiredMixin."""

    def has_permission(self):
        if self.request.user.is_staff == True:
            return True
        else:
            return super().has_permission()
        
class MyLoginView(LoginView):
    template_name = "admin/admin_login.html"
    form_class = LoginForm
    next_page = "user:user-list"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("user:user-list")
        return super().get(request, *args, **kwargs)


class MyUserListView(MyListView):
    template_name = "admin/user_list.html"
    model = User

    def get_queryset(self):
        """Override queryset to add extra functionality"""
        return self.model.objects.filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["opts"] = self.model._meta
        context_data["count"] = self.model.objects.count()
        return context_data


class UserListAjaxView(View, HasPermissionsMixin):
    """
    Ajax-Pagination view for Userlisting
    """

    model = User

    def get_queryset(self):
        queryset = self.model.objects.exclude(id=self.request.user.id)
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

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        
        if self.search:
            return qs.filter(
                Q(email__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(username__icontains=self.search)
                | Q(last_name__icontains=self.search),
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for user in qs:
            data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_active": self._get_check(user.is_active),
                    "is_staff": self._get_check(user.is_staff),
                    "last_login": user.last_login.strftime("%d/%m/%Y %I:%M %p") if user.last_login else None,
                    "date_joined": user.date_joined.strftime("%d/%m/%Y %I:%M %p"),
                    "action": self._get_actions(user),
                }
            )
        return data
    
    def get(self, request, *args, **kwargs):
       
        context_data = {}
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        queryset = self.get_queryset()[start:start + length]
        context_data["data"] = self.prepare_results(queryset)

        return JsonResponse(context_data)
    

class CreateUserView(MyCreateView):
    model = User

    def get_form_class(self):
            return CreateUserForm

    template_name = "admin/user_create.html"

class MyUserDeleteView(View):

    def get(self, request, pk):
        try:
            # Retrieve the user by primary key
            user = User.objects.get(id=pk)

            # Delete the user
            user.delete()

            # delete_user_task.delay(user_id=pk)
            messages.success(self.request, f"User deleted.")
            return HttpResponseRedirect(reverse("user:user-list"))

        except User.DoesNotExist:
            messages.error(self.request, "User does not exist")
            return HttpResponseRedirect(reverse("user:user-list"))

        except Exception as e:
            return HttpResponseRedirect(reverse("user:user-list"))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    
class UpdateUserView(MyUpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = "admin/user_update.html"

    def get_initial(self) -> dict:
        initial = super().get_initial()
        return initial
    
class UserProfileView(MyUpdateView):
    model = User
    template_name = "admin/user_detail.html"
    # form_class = UpdateUserForm
    fields = ['username','first_name', 'last_name', 'email']