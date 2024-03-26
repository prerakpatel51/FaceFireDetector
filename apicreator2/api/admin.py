from django.contrib import admin
from .models import User, URL, Image

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'unique_id']

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'url', 'camera_id']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'image']
