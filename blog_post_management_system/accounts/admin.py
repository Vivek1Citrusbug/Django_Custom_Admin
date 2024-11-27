from django.contrib import admin
from .domain.models import UserProfile

class AdminProfileClass(admin.ModelAdmin):
    list_display = ('user','bio','profile_picture')
    

admin.site.register(UserProfile,AdminProfileClass)
