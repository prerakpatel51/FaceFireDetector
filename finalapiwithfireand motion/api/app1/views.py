import base64

from urllib.parse import urlparse
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotAllowed
from rest_framework import views, status
from rest_framework.response import Response

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User_Id,Camera_Id,UploadUrlAndImages,Status_Process,KnownLog,UnknownLog,UploadUrlFireDetection,UploadMotionUrl
import hashlib
import uuid,json,os,requests
import cv2
import face_recognition
import os
import pickle
import multiprocessing
from main4 import x
import signal
from datetime import datetime
from firedetection import fire
from motion import motion

@csrf_exempt
def create_user_id(request):
    if request.method == 'POST':
       
        name=request.POST.get('name')
        email=request.POST.get('email')
        print(name)
        print(email)
        user_id = hashlib.md5((name + email).encode()).hexdigest()

        try:
            existing_user = User_Id.objects.get(name=name, email=email)
            return JsonResponse({'message': 'User already exists', 'user_id': existing_user.user_id},status=200)
        except User_Id.DoesNotExist:
            # Save the unique ID to the database
            User_Id.objects.create(name=name, email=email, user_id=user_id)
            # Return the unique ID as a response
            return JsonResponse({'user_id': user_id},status=201)
        

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def create_camera_id(request):
    if request.method == 'POST':
        user_id= request.POST.get('user_id')
        print(user_id)
        if not User_Id.objects.filter(user_id=user_id).exists():
            return JsonResponse({'error': 'User_id does not exist'},status=404)

        # Generate a unique ID based on the email and name
        camera_id = uuid.uuid4()

        # Save the unique ID to the database
        Camera_Id.objects.create(user_id=user_id,camera_id=camera_id)
        
        # Return the unique ID as a response
        return JsonResponse({'camera_id': camera_id},status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def upload_imagesurl_and_url_face_detection(request):
    if request.method == 'POST':
        camera_id = request.POST.get('camera_id')
        url = request.POST.get('url')
        image_urls = request.POST.get('image_urls')
        
        # print(image_urls)
        

        # Check if the record already exists
        try:
            existing_record = UploadUrlAndImages.objects.get(camera_id=camera_id)
            # Update the existing record
            existing_record.url = url
            existing_record.image_urls = image_urls
            existing_record.save()
        except UploadUrlAndImages.DoesNotExist:
            # Create a new record
            UploadUrlAndImages.objects.create(camera_id=camera_id, url=url, image_urls=image_urls)
        
        return JsonResponse({'message': 'Images uploaded successfully'},status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)













def get_images_save_encode(camera_id):
    try:
        data = UploadUrlAndImages.objects.get(camera_id=camera_id)
        image_urls = json.loads(data.image_urls)
        
        folder_path = os.path.join('api/all_images', str(camera_id))
        os.makedirs(folder_path, exist_ok=True)
        
        for i, url in enumerate(image_urls):
            try:
                response = requests.get(url)
                
                if response.status_code == 200:
                   
                    filename = url.split('/')[-2] 
                    print(url)
                    
                    image_path = os.path.join(folder_path, filename)
                    with open(image_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Image saved: {image_path}")
                else:
                    print(f"Failed to download image from {url}")
            except Exception as e:
                print(f"Error downloading image from {url}: {e}")
    except Exception as e:
            print(f"Error downloading image from : {e}")





def encode_faces_for_camera(extract_dir, camera_id, encoder_folder):
    # Get the folder path for the specified camera_id
    folder_path = os.path.join(extract_dir, str(camera_id))
    
    if not os.path.exists(folder_path):
        print(f"Folder for camera {camera_id} not found.")
        return

    # List all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if len(image_files) == 0:
        print(f"No images found for camera {camera_id}.")
        return

    encodeListKnown = []
    empIds = []

    for image_file in image_files:
        # Load the image
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)
        # Convert the image to RGB format (required by face_recognition library)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Encode the face
        encode = face_recognition.face_encodings(rgb_img)[0]
        # Append the encoding and corresponding image name to lists
        encodeListKnown.append(encode)
        empIds.append(os.path.splitext(image_file)[0])

    # Save the encodings and image names to a pickle file
    encodeListKnownWithIds = [encodeListKnown, empIds]

    # Create the encodings folder if it doesn't exist
    os.makedirs(encoder_folder, exist_ok=True)

    encoder_name = os.path.join(encoder_folder, f"{camera_id}.pkl")
    with open(encoder_name, 'wb') as file:
        pickle.dump(encodeListKnownWithIds, file)

    print(f"Encoding completed for camera {camera_id}. Encodings saved to", encoder_name)



@csrf_exempt
def start_camera_face_detection(request):
    if request.method == 'POST':
        try:
            camera_id = request.POST.get('camera_id')
            status_process_exists = Status_Process.objects.filter(camera_id=camera_id,detection_type='Face').exists()
            if status_process_exists:
                return JsonResponse({'message': 'Process already started'},status=400)
            else:
                
                existing_record = UploadUrlAndImages.objects.get(camera_id=camera_id)
                url = existing_record.url
                encoder_name = f"api/encodings/{camera_id}.pkl"
                get_images_save_encode(camera_id)
                encode_faces_for_camera('api/all_images', camera_id, "api/encodings")
                processes = multiprocessing.Process(target=x, args=[camera_id, url, encoder_name])
                processes.start()
                process_id = str(processes.pid)
                status_process=Status_Process.objects.create(process_id=process_id, camera_id=camera_id, status=True,detection_type='Face')
                status_process.save()
                
                return JsonResponse({'message': 'Started successfully'},status=200)
        except Status_Process.DoesNotExist:
            return JsonResponse({'message': 'No process found for the given camera ID'})
        except Exception as e:
            return JsonResponse({'error': str(e)},status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def stop_camera_face_detection(request):
    if request.method=='POST':
        try:
            camera_id=request.POST.get('camera_id')
            status_process = Status_Process.objects.get(camera_id=camera_id,detection_type='Face')
            print(status_process.process_id)
            if status_process.status==1:
               
                process_id = status_process.process_id
                os.kill(int(process_id), signal.SIGTERM)
                status_process.delete()
                
                return JsonResponse({'message': 'Process stopped successfully'},status=200)
            else:
                return JsonResponse({'message': 'No running process to stop'},status=400)     
        except Status_Process.DoesNotExist:
            return JsonResponse({'message': 'No process found for the given camera ID'},status=404)
    return HttpResponseNotAllowed(['POST'])



def getlog(request):
    if request.method=='GET':
        user_id=request.GET.get('user_id')
        
        if request.GET.get('start_time') and request.GET.get('end_time'):
            start_time=request.GET.get('start_time')
            end_time=request.GET.get('end_time')
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            print(start_time)
            print(end_time)
            check=Camera_Id.objects.filter(user_id=user_id).exists()
            if check:
                
                camera_ids = Camera_Id.objects.filter(user_id=user_id).values_list('camera_id', flat=True)
                all_known_logs = []
                all_unknown_logs=[]
                # Iterate over each camera_id and fetch the logs
                for camera_id in camera_ids:
                    known_logs = KnownLog.objects.filter(camera_id=camera_id,time__range=(start_time, end_time))
                    known_logs_list = list(known_logs.values())
                    all_known_logs.extend(known_logs_list)
                    
                    unknown_logs=UnknownLog.objects.filter(camera_id=camera_id,detection_time__range=(start_time,end_time))
                    unknown_logs_list=list(unknown_logs.values())
                    all_unknown_logs.extend(unknown_logs_list)
                    
                for log in all_unknown_logs:
                        log['image_data'] = base64.b64encode(log['image_data']).decode('utf-8')
                        
                return JsonResponse({'known_logs': all_known_logs,'unknown_log':all_unknown_logs},status=200)
            else:
                return JsonResponse({"error":'NO data found in the DATABASE'},status=404)
            
        else:
            check=Camera_Id.objects.filter(user_id=user_id).exists()
            if check:
                
                camera_ids = Camera_Id.objects.filter(user_id=user_id).values_list('camera_id', flat=True)
                all_known_logs = []
                all_unknown_logs=[]
                # Iterate over each camera_id and fetch the logs
                for camera_id in camera_ids:
                    known_logs = KnownLog.objects.filter(camera_id=camera_id)
                    known_logs_list = list(known_logs.values())
                    all_known_logs.extend(known_logs_list)
                
                    unknown_logs=UnknownLog.objects.filter(camera_id=camera_id)
                    unknown_logs_list=list(unknown_logs.values())
                    all_unknown_logs.extend(unknown_logs_list)
                    
                for log in all_unknown_logs:
                        log['image_data'] = base64.b64encode(log['image_data']).decode('utf-8')
                        
                
                return JsonResponse({'known_logs': all_known_logs,'unknown_log':all_unknown_logs})
        
            else:
                return JsonResponse({"error":'NO data found in the DATABASE'},status=404)
    return HttpResponseNotAllowed(['GET'])
        
        
        
        

@csrf_exempt
def upload_url_fire_detection(request):
    if request.method == 'POST':
        camera_id = request.POST.get('camera_id')
        url = request.POST.get('url')
        check=Camera_Id.objects.filter(camera_id=camera_id).exists()
        if check:
            # Check if the record already exists
            try:
                existing_record = UploadUrlFireDetection.objects.get(camera_id=camera_id)
                # Update the existing record
                existing_record.url = url
            
                existing_record.save()
            except UploadUrlFireDetection.DoesNotExist:
                # Create a new record
                UploadUrlFireDetection.objects.create(camera_id=camera_id, url=url)
            return JsonResponse({'message': 'Url uploaded successfully'},status=200)
            
        else:
            
            return JsonResponse({'Error': 'No such camera_id found'},status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

       
       
       
       

@csrf_exempt
def start_camera_fire_detection(request):
    if request.method == 'POST':
        try:
            camera_id = request.POST.get('camera_id')
            status_process_exists = Status_Process.objects.filter(camera_id=camera_id,detection_type='Fire').exists()
            if status_process_exists:
                return JsonResponse({'message': 'Process already started'},status=400)
            else:
                
                existing_record = UploadUrlFireDetection.objects.get(camera_id=camera_id)
                url = existing_record.url
               
                
                processes = multiprocessing.Process(target=fire, args=[camera_id, url,])
                processes.start()
                process_id = str(processes.pid)
                status_process=Status_Process.objects.create(process_id=process_id, camera_id=camera_id, status=True,detection_type='Fire')
                status_process.save()
                
                return JsonResponse({'message': 'Started successfully'},status=200)
        except Status_Process.DoesNotExist:
            return JsonResponse({'message': 'No process found for the given camera ID'})
        except Exception as e:
            return JsonResponse({'error': str(e)},status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




    



@csrf_exempt
def stop_camera_fire_detection(request):
    if request.method=='POST':
        try:
            camera_id=request.POST.get('camera_id')
            status_process = Status_Process.objects.get(camera_id=camera_id,detection_type='Fire')
            print(status_process.process_id)
            if status_process.status==1:
               
                process_id = status_process.process_id
                os.kill(int(process_id), signal.SIGTERM)
                status_process.delete()
                
                return JsonResponse({'message': 'Process stopped successfully'},status=200)
            else:
                return JsonResponse({'message': 'No running process to stop'},status=400)     
        except Status_Process.DoesNotExist:
            return JsonResponse({'message': 'No process found for the given camera ID'},status=404)
    return HttpResponseNotAllowed(['POST'])






@csrf_exempt
def upload_url_motion_detection(request):
    if request.method == 'POST':
        camera_id = request.POST.get('camera_id')
        url = request.POST.get('url')
        check=Camera_Id.objects.filter(camera_id=camera_id).exists()
        if check:
            # Check if the record already exists
            try:
                existing_record = UploadMotionUrl.objects.get(camera_id=camera_id)
                # Update the existing record
                existing_record.url = url
            
                existing_record.save()
            except UploadMotionUrl.DoesNotExist:
                # Create a new record
                UploadMotionUrl.objects.create(camera_id=camera_id, url=url)
            return JsonResponse({'message': 'Url uploaded successfully'},status=200)
            
        else:
            
            return JsonResponse({'Error': 'No such camera_id found'},status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)





  

@csrf_exempt
def start_camera_motion_detection(request):
    if request.method == 'POST':
        try:
            camera_id = request.POST.get('camera_id')
            status_process_exists = Status_Process.objects.filter(camera_id=camera_id,detection_type='Motion').exists()
            if status_process_exists:
                return JsonResponse({'message': 'Process already started'},status=400)
            else:
                
                existing_record = UploadMotionUrl.objects.get(camera_id=camera_id)
                url = existing_record.url
                processes = multiprocessing.Process(target=motion, args=[ url,camera_id])
                processes.start()
                process_id = str(processes.pid)
                status_process=Status_Process.objects.create(process_id=process_id, camera_id=camera_id, status=True,detection_type='Motion')
                status_process.save()
                
                return JsonResponse({'message': 'Started successfully'},status=200)
        except Status_Process.DoesNotExist:
            return JsonResponse({'message': 'No process found for the given camera ID'})
        except Exception as e:
            return JsonResponse({'error': str(e)},status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




     
       

@csrf_exempt
def stop_camera_motion_detection(request):
    if request.method=='POST':
        try:
            camera_id=request.POST.get('camera_id')
            status_process = Status_Process.objects.get(camera_id=camera_id,detection_type='Motion')
            print(status_process.process_id)
            if status_process.status==1:
                process_id = status_process.process_id
                os.kill(int(process_id), signal.SIGTERM)
                status_process.delete()
                return JsonResponse({'message': 'Process stopped successfully'},status=200)
            else:
                return JsonResponse({'message': 'No running process to stop'},status=400)     
        except Status_Process.DoesNotExist:
            return JsonResponse({'message': 'No process found for the given camera ID'},status=404)
    return HttpResponseNotAllowed(['POST'])
