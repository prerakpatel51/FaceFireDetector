
import cv2
import face_recognition
import pickle
import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import shutil

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/Users/prerak/Desktop/new approach/apicreator2/dbkey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rtspcode-default-rtdb.firebaseio.com'
})

def get_data_from_firebase(node):
    ref = db.reference(node)
    return ref.get()

def download_and_store_image(image_url, camera_id, image_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_path = f"/Users/prerak/Desktop/new approach/apicreator2/all_images/{camera_id}/"
        os.makedirs(image_path, exist_ok=True)
        image_name = f"{image_name}.png"  # Append .png to the image name
        with open(os.path.join(image_path, image_name), 'wb') as f:
            f.write(response.content)
        return os.path.join(image_path, image_name)
    else:
        return None

def encode_faces(extract_dir, encoder_dir):
    folderPath = extract_dir

    PathList = os.listdir(folderPath)

    for folder in PathList:
        subFolderPath = os.path.join(folderPath, folder)
        if not os.path.isdir(subFolderPath):
            continue
        subPathList = os.listdir(subFolderPath)
        imgList = []
        empIds = []
        
        for path in subPathList:
            full_path = os.path.join(subFolderPath, path)
            img = cv2.imread(full_path)
            if img is None:
                print(f"Failed to load image: {path}")
                continue
            imgList.append(img)
            empIds.append(path)  # Using the image name as camera_id
            print(empIds)
        def findencodings(imagesList):
            encodeList = []
            for img in imagesList:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        print(f"Encoding images in folder {folder}...")
        encodeListKnown = findencodings(imgList)
        encodeListKnownWithIds=[encodeListKnown,empIds]
        print("Encoding completed")

        encoder_name = os.path.join(encoder_dir, f"{folder}.pkl")
        os.makedirs(os.path.dirname(encoder_name), exist_ok=True)  # Create the directory if it doesn't exist
        with open(encoder_name, 'wb') as f:
            pickle.dump(encodeListKnownWithIds, f)

    print("All images encoded and saved.")
    shutil.rmtree(extract_dir)

    print("all_images folder deleted.")

extract_dir = "/Users/prerak/Desktop/new approach/apicreator2/all_images"  # Path to the directory containing folders of images
encoder_dir = "/Users/prerak/Desktop/new approach/apicreator2/encodings"  # Directory to save the encoded faces

# Get data from Firebase
data = get_data_from_firebase('all_unique_ids')

# Process the data
for unique_id, value in data.items():
    urls = value.get('urls', {})
    for camera_id, details in urls.items():
        images = details.get('images', [])
        for image_details in images:
            image_url = image_details.get('image_url')
            image_name = image_details.get('image_name')
            image_path = download_and_store_image(image_url, camera_id, image_name)
            if image_path:
                print(f"Image saved at: {image_path}")

# Encode faces
encode_faces(extract_dir, encoder_dir)
