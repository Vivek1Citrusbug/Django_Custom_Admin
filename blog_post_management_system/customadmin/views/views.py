from datetime import timezone
import re
from typing import Dict
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
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
    next_page = "user-list"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("user-list")
        return super().get(request, *args, **kwargs)


# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect("customadmin:admin_login")


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


# class MyUserDeleteView(View):
#     def get(self, request, pk):
#         try:
#             delete_user_task.delay(user_id=pk)
#             messages.success(self.request, f"User will deleted.")
#             return HttpResponseRedirect(reverse("user:user-list"))

#         except User.DoesNotExist:
#             log.error(
#                 f"Error at MyUserDeleteView {str(e)} at line {e.__traceback__.tb_lineno}"
#             )
#             messages.error(self.request, "User does not exist")
#             return HttpResponseRedirect(reverse("user:user-list"))

#         except Exception as e:
#             log.error(
#                 f"Error at MyUserDeleteView {str(e)} at line {e.__traceback__.tb_lineno}"
#             )
#             return HttpResponseRedirect(reverse("user:user-list"))

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(self.__class__, self).dispatch(request, *args, **kwargs)





# class MyLoginView(LoginView):
#     template_name = "admin/admin_login.html"
#     form_class = LoginForm
#     next_page = "company:company-list"

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect("company:company-list")
#         return super().get(request, *args, **kwargs)



# class ForgotPassword(View):
#     def get(self, request):
#         return render(request, "admin/forgot_password.html")

#     def post(self, request):
#         email = request.POST.get("email")
#         user = User.objects.filter(email=email).filter().first()

#         if user:
#             if (not user.reset_password_token) or (
#                 user.reset_token_expiration < timezone.now()
#             ):
#                 token = uuid.uuid4()
#                 user.reset_password_token = str(token)
#             user.reset_token_expiration = timezone.now() + timezone.timedelta(
#                 minutes=int(os.getenv("PASSWORD_CHANGE_TOKEN_EXPIRATION", 10))
#             )
#             user.save()

#             context = {
#                 "username": user.username,
#                 "reset_password_url": f"{os.getenv('HOST_NAME')}admin/reset-password/{user.reset_password_token}",
#             }
#             send_forgot_password_email_custom_admin(
#                 context=context, recipient_list=[user.email]
#             )
#             messages.success(request, "Email Has Been Sent For Reset Password")
#             return render(request, "admin/forgot_password.html")
#         else:
#             messages.error(request, "User with given email doesn't exist")
#             return render(request, "admin/forgot_password.html")


# class ResetTokenView(View):
#     def get(self, request, token):
#         user = User.objects.filter(reset_password_token=token).first()
#         if user:
#             if user.reset_token_expiration > timezone.now():
#                 request.session["forgot_password_email"] = user.email
#                 return render(request, "admin/change_password.html")
#             else:
#                 return HttpResponse("Token Expired")
#         else:
#             return HttpResponse("Invalid Token")


# class ChangePasswordView(View):
#     def get(self, request):
#         return render(request, "admin/change_password.html")

#     def post(self, request):
#         email = self.request.session.get("forgot_password_email")
#         if email is None:
#             return redirect("customadmin:forgot_password")
#         user = User.objects.filter(email=email).first()
#         new_password = request.POST.get("new_password")
#         confirm_new_password = request.POST.get("confirm_new_password")
#         if not re.match(settings.PASSWORD_REGEX, new_password):
#             messages.error(request, "Please enter a strong password")
#             return render(request, "admin/change_password.html")

#         if new_password == confirm_new_password:
#             user.set_password(new_password)
#             user.reset_password_token = None
#             user.reset_token_expiration = None
#             user.save()
#             del self.request.session["forgot_password_email"]
#             messages.success(request, "Your Password Has Been Successfully Changed")
#             return redirect("customadmin:admin_login")
#         else:
#             messages.error(
#                 request, "New password and confirm new password did not match"
#             )
#             return render(request, "admin/change_password.html")


# class CreateUserView(MyCreateView):
#     model = User
#     template_name = "admin/user_create.html"
#     def get_form_class(self):
#             return CreateUserForm

# class UserProfileView(MyUpdateView):
#     model = User
#     template_name = "admin/user_update.html"


# class UpdateUserView(MyUpdateView):
#     model = User
#     form_class = UpdateUserForm
#     template_name = "admin/user_update.html"

#     def get_initial(self) -> dict:
#         initial = super().get_initial()
#         company = (
#             Company.objects.filter(pk=self.get_object().company_id).first()
#             or "deleted company"
#         )

#         level = ActivityLevel.objects.filter(
#             pk=self.get_object().activity_level_id
#         ).first()

#         initial["company_id"] = company
#         initial["activity_level_id"] = level.name if level else "not selected"
#         return initial