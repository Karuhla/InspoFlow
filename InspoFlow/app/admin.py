from django.contrib import admin
from .models import Category, Image, Like, Comment, Board
from .models import Profile

# Register your models here.

class PictureInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [PictureInline] 

admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Board)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture_url', 'created_at')
    search_fields = ('user__username',)