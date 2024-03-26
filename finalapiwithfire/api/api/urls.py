"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user_id',views.create_user_id,name="create user id"),
    path('create_camera_id',views.create_camera_id,name='create_camera_id'),
    path('upload_imageurl_url',views.upload_imagesurl_and_url_face_detection,name='upload images'),
    path('startcamera_face_detection',views.start_camera_face_detection,name='start_camera'),
    path('stopcamera_face_detection',views.stop_camera_face_detection),
    path('getlog_face_detection',views.getlog,name='getlog'),
    path('upload_url_fire_detection',views.upload_url_fire_detection,name='urlfireupload'),
    path('startcamera_fire_detection',views.start_camera_fire_detection,name='firedetectionstart'),
    path('stopcamera_fire_detection',views.stop_camera_fire_detection,name='firedetectionstop'),
    
]

