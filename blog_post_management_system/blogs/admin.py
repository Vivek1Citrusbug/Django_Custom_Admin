from django.contrib import admin
from django.contrib.admin import AdminSite
from blogs.domain.models import BlogPost
from comments.domain.models import UserComments
from likes.domain.models import Like

class CommentInline(admin.TabularInline):
    model = UserComments
    extra = 0
    
class LikesInline(admin.TabularInline):
    model = Like
    extra= 0

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline,LikesInline]
    list_display = ['title','content','author', 'date_published']
    list_filter = ['author', 'date_published']
    search_fields = ['title','content','author', 'date_published']
    

admin.site.register(BlogPost,BlogAdmin)
