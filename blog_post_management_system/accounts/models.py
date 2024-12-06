from django.db import models
from django.contrib.auth.models import User  
from django.utils.timezone import now

class UserProfile(models.Model):
    """This model is joined with built in User model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.TextField(blank=True)  
    profile_picture = models.ImageField(upload_to='profiles/profile_pictures/', blank=True, null=True)  

    # def __str__(self):
    #     return f"{self.user.username}'s Profile"


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="password_reset_token")
    token = models.CharField(max_length=255, blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)

    def is_token_valid(self):
        return self.expiration and self.expiration > now()

