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
from customadmin.views.generics import MyCreateView,MyUpdateView,MyListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from accounts.models import UserProfile
from django.views.generic import DetailView, UpdateView
from customadmin.forms.users import UserProfileForm
from django.urls import reverse_lazy

class MyLoginView(LoginView):
    template_name = "admin/admin_login.html"
    form_class = LoginForm
    next_page = "user:user-list"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  
            if not request.user.is_superuser:  
                return redirect('user:admin_login')  
            return redirect(self.next_page) 
        return super().get(request, *args, **kwargs) 
    
    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser: 
            login(self.request, user)  
            return super().form_valid(form)  
        else:
            form.add_error(None, "Please enter a correct username and password.")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("user:admin_login")
    
class MyUserListView(MyListView):
    template_name = "admin/user_list.html"
    model = User

    def get_queryset(self):
        """Override queryset to add extra functionality"""
        return self.model.objects.filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(context_data,"###################")
        context_data["opts"] = self.model._meta
        print( context_data["opts"],"###################")
        context_data["count"] = self.model.objects.count()

        return context_data


class UserListAjaxView(View, HasPermissionsMixin):
    """
    Ajax-Pagination view for Userlisting
    """
    template_name = "admin/user_list.html"
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

    def prepare_results(self, qs):
        """Prepare final result data here."""
        company_instances = UserProfile.objects.all().values_list("pk", "bio", "profile_picture", "user_id")
        company_name_dict = {str(x[3]): [x[0], x[1], x[2]] for x in company_instances}
        

        data = []
        
        for user in qs:
            profile_picture = company_name_dict.get(str(user.id), [None, None, None])[2]
            if profile_picture:
                profile_picture = "/images/"+profile_picture

            data.append(
                {
                    "id": user.id,
                    "profile_picture":profile_picture,
                    "username": [user.username],
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
        draw = int(request.GET.get("draw", 1))
        search_value = request.GET.get("search[value]", "").strip()
        queryset = self.model.objects.exclude(id=request.user.id)

        if search_value:
            queryset = queryset.filter(
                Q(username__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value)
            )

        total_records = self.model.objects.exclude(id=request.user.id).count()
        filtered_records = queryset.count()
        queryset = queryset[start:start + length]
        data = self.prepare_results(queryset)

        # return context
        context_data["data"] = data
        # context_data["columns"] = list(data[0].keys()) if data else []
        context_data["draw"] = draw
        context_data["recordsTotal"] = total_records
        context_data["recordsFiltered"] = filtered_records

        return JsonResponse(context_data)
    

class CreateUserView(MyCreateView):
    model = User
    def get_form_class(self):
            return CreateUserForm

    template_name = "admin/user_create.html"

class MyUserDeleteView(View):

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user.delete()
            print("Inside delete view #########################")
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
    template_name = 'admin/user_update.html'
    success_url = reverse_lazy('user:user-list') 

    def get_object(self):
        user = super().get_object()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user.profile = user_profile
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UserProfileForm(instance=self.object.profile)
        return context

    def form_valid(self, form):
        user_form = form.save(commit=False)
        user_form.save()
        profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=self.object.profile)
        if profile_form.is_valid():
            profile_form.save()
        return redirect(self.success_url)


class UserProfileView(MyUpdateView):
    model = User
    template_name = "admin/user_detail.html"
    fields = ['username','first_name', 'last_name', 'email']

    def get_object(self):
        user = super().get_object()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user.profile = user_profile
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UserProfileForm(instance=self.object.profile)
        return context
