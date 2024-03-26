import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
import requests
from multiprocessing import Process
import time,os


def get_data_from_firebase(node):
    # Initialize Firebase Admin SDK
   

    # Reference to the specified node in your database
    ref = db.reference(node)

    # Get the data from the database
    data = ref.get()

    # Return the data
    return data

# Example usage
data = get_data_from_firebase('all_unique_ids')
# print(data)









def extract_camera_data(data):
    camera_data = {}
    for unique_id, value in data.items():
        urls = value.get('urls', {})
        for camera_id, details in urls.items():
            url = details.get('url')
            camera_data[camera_id] = url
    return camera_data


from main4 import x
if __name__ == '__main__':
    processes = []
    camera_data = extract_camera_data(data)
    for camera_id, url in camera_data.items():
        print(f"Camera ID: {camera_id}, URL: {url}")
         
        encoder_name=f"/Users/prerak/Desktop/new approach/apicreator2/encodings/{camera_id}.pkl"
        if os.path.exists(encoder_name):
            p = Process(target=x, args=(camera_id, url,encoder_name))
            processes.append(p)
            p.start()
        
    
    
