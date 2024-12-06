from django.contrib import admin
from .models import UserProfile,PasswordResetToken

admin.site.register(UserProfile)
admin.site.register(PasswordResetToken)
