from typing import Any

from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

# from just_move_python.domain.user.models import User, UserRoleNames

from ..mixins import HasPermissionsMixin, ModelOptsMixin
from ..templatetags.misc_filters import admin_urlname

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

find_element = lambda arr, target: target in arr


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


class SuccessMessageMixin(object):
    """CBV mixin which adds a success message on form save."""

    success_message = ""

    def get_success_message(self, message: str):
        return self.success_message

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message()
        if success_message:
            messages.success(self.request, success_message)
        return response


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
        return redirect("customadmin:admin_login")


class MyListView(
    MyLoginRequiredMixins,
    MyPermissionRequiredMixin,
    ModelOptsMixin,
    HasPermissionsMixin,
    ListView,
):
    """ListView CBV with LoginRequiredMixin and PermissionRequiredMixin."""

    def has_permission(self):
        if self.request.user.is_staff == True:
            return True
        else:
            return super().has_permission()


class MyCreateView(
    MyLoginRequiredMixins,
    MyPermissionRequiredMixin,
    ModelOptsMixin,
    SuccessMessageMixin,
    HasPermissionsMixin,
    CreateView,
):
    """CreateView CBV with LoginRequiredMixin, PermissionRequiredMixin
    and SuccessMessageMixin."""

    def get_success_message(self):
        return MSG_CREATED.format(self.object)

    def get_success_url(self):
        opts = self.model._meta
        return reverse(admin_urlname(opts, "list"))

    def has_permission(self):
        if self.request.user.is_staff == True:
            return True
        else:
            return super().has_permission()

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not self.request.user.is_superuser:
            messages.error(
                self.request,
                "You don't have permission to create company",
            )
            return HttpResponseRedirect(reverse("company:company-list"))
        return super().get(request, *args, **kwargs)


class MyDeleteView(
    MyLoginRequiredMixins,
    MyPermissionRequiredMixin,
    ModelOptsMixin,
    SuccessMessageMixin,
    HasPermissionsMixin,
    DeleteView,
):
    def get_success_message(self):
        return MSG_DELETED.format(self.object)

    def has_permission(self):
        if self.request.user.is_staff == True:
            return True
        else:
            return super().has_permission()


class MyUpdateView(
    LoginRequiredMixin,
    MyPermissionRequiredMixin,
    SuccessMessageMixin,
    ModelOptsMixin,
    HasPermissionsMixin,
    UpdateView,
):
    """UpdateView CBV with LoginRequiredMixin, PermissionRequiredMixin
    and SuccessMessageMixin."""

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            return super().get(request, *args, **kwargs)
        except ValidationError:
            messages.error(request=request, message="Invalid URL")
            return redirect("company:company-list")

    def get_permission_required(self):
        """Default to view and change perms."""
        opts = self.model._meta
        codename_view = get_permission_codename("view", opts)
        codename_change = get_permission_codename("change", opts)
        view_perm = f"{opts.app_label}.{codename_view}"
        change_perm = f"{opts.app_label}.{codename_change}"
        perms = (view_perm, change_perm)
        return perms

    def get_success_message(self):
        return MSG_UPDATED.format(self.object)

    def get_success_url(self):
        opts = self.model._meta
        return reverse(admin_urlname(opts, "list"))

    def has_permission(self):
        if self.request.user.is_staff == True:
            return True
        else:
            return super().has_permission()
