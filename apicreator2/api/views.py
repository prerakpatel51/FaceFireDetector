from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import User,URL
from .serializers import User1Serializer
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer


from django.views.decorators.csrf import csrf_exempt
@api_view(['GET','PUT'])
@csrf_exempt
def get_unique_id(request):
    if request.method == 'GET':
        all_users = User.objects.all()
        serializer = User1Serializer(all_users, many=True)
        return Response(serializer.data)
    if request.method=='PUT':
        data = json.loads(request.body)
        user_name = data.get('name')
        new_unique_id = data.get('unique_id')
        if user_name is None or new_unique_id is None:
            return JsonResponse({'error': 'Both user_id and unique_id are required'}, status=400)
        
        try:
            user = User.objects.get(name=user_name)
            user.unique_id = new_unique_id
            user.save()
            return JsonResponse({'message': 'Unique ID updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
  

# @api_view(['GET','PUT'])
# @csrf_exempt
# def camera_id(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         data = json.loads(request.body)
#         url = data.get('url')
#         camera_id = data.get('camera_id')
#         # updated_data = request.data.get('updated_data', [])
#         # for item in updated_data:
#         user = URL.objects.get(url=url,camera_id=camera_id)
#         serializer = UserSerializer(user, data=camera_id, partial=True)
#         if serializer.is_valid():
#                 serializer.save()
#         else:
#         # print("done")
#             return Response(serializer.errors, status=400)
        
#         return Response("Data updated successfully")
    
#     return Response("Invalid request method", status=400)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['GET'])
def camera_id(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    
    
@csrf_exempt
@api_view(['PUT']) 
def get_camera_id(request):    
    if request.method == 'PUT':
        print("hii")
        data = json.loads(request.body)
        url = data.get('url')
        camera_id = data.get('camera_id')
        print(url,camera_id)
        url_obj = URL.objects.get(url=url)
        url_obj.camera_id = camera_id
        url_obj.save()
        print("saved")
       
        return Response("Data updated successfully")
       
    else:
        return Response("Invalid request method", status=400)
