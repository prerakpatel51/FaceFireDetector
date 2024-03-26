from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User_Id, Camera_Id, UploadUrlAndImages, Status_Process, KnownLog, UnknownLog,Fire_Log,UploadUrlFireDetection

# Register your models here.

@admin.register(User_Id)
class User_IdAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user_id']

@admin.register(Camera_Id)
class Camera_IdAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'camera_id']

@admin.register(UploadUrlAndImages)
class UploadUrlAndImagesAdmin(admin.ModelAdmin):
    list_display = ['camera_id', 'url', 'image_urls']

@admin.register(Status_Process)
class Status_ProcessAdmin(admin.ModelAdmin):
    list_display = ['process_id', 'camera_id', 'status']


from django.contrib import admin
from .models import KnownLog, UnknownLog

@admin.register(KnownLog)
class KnownLogAdmin(admin.ModelAdmin):
    list_display = ['camera_id', 'name', 'time']
    search_fields = ['camera_id', 'name', 'time']

@admin.register(UnknownLog)
class UnknownLogAdmin(admin.ModelAdmin):
    list_display = ['camera_id', 'image_name', 'detection_time']
    search_fields = ['camera_id', 'image_name', 'detection_time']






@admin.register(Fire_Log)
class Fire_LogAdmin(admin.ModelAdmin):
    list_display = ['detection_time', 'camera_id']

@admin.register(UploadUrlFireDetection)
class UploadUrlFireDetectionAdmin (admin.ModelAdmin):
    list_display = [ 'camera_id','url']
