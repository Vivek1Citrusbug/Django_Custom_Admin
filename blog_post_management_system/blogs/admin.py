from django.contrib import admin
from django.contrib.admin import AdminSite
from blogs.domain.models import BlogPost
from comments.domain.models import UserComments
from likes.domain.models import Like


class CommentInline(admin.TabularInline):
    """Admin comment class for inline functionality"""

    model = UserComments
    extra = 0


class LikesInline(admin.TabularInline):
    """Admin Like class for inline functionality"""

    model = Like
    extra = 0


# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    """Class handles view of BlogPost model in Admin site"""

    inlines = [CommentInline, LikesInline]
    list_display = ["title", "content", "author", "date_published"]
    list_filter = ["author", "date_published"]
    search_fields = ["title", "content", "author", "date_published"]


admin.site.register(BlogPost, BlogAdmin)
