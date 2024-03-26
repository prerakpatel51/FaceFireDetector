import requests
import uuid,json
import time
import cv2
import face_recognition
import pickle
import os
import requests







def create_table_if_not_exists(conn):
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS all_unique_ids (
                
                unique_id VARCHAR(255)PRIMARY KEY,
                urls JSONB
            )
        """)
        conn.commit()
        cursor.close()
        
        
def insert_into_all_unique_ids(conn, unique_id, urls):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO all_unique_ids (unique_id, urls) VALUES (%s, %s)
        """,
        (unique_id,json.dumps(urls))
    )
    conn.commit()
    cursor.close()
    
    
def update_urls(conn, unique_id, urls):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE all_unique_ids
        SET urls = %s
        WHERE unique_id = %s
        """,
        (json.dumps(urls), unique_id)
    )
    conn.commit()
    cursor.close()


def check_unique_id_exists(conn, unique_id):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT EXISTS(SELECT 1 FROM all_unique_ids WHERE unique_id = %s)
        """,
        (unique_id,)
    )
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists
    
import psycopg2
conn=psycopg2.connect(
    dbname='face',
    user='face',
    password='root',
    host='localhost',
    port=5432
)
create_table_if_not_exists(conn)




response=requests.get("http://127.0.0.1:8000")
if response.status_code==200:
    data=response.json()
    # print(data)
    for user in data:
        if user['unique_id']==None:
                
            unique_factor = f"{user['email']}-{user['name']}"
            # Generate a unique ID based on the unique factor
            new_unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_factor))

            user['unique_id'] = new_unique_id
            
            updated_response=requests.put("http://127.0.0.1:8000",json={'name':user['name'],'unique_id': new_unique_id})
            insert_into_all_unique_ids(conn,new_unique_id,None)
            
    # print("----------------------------",data,"---------------------------------------------")
    
   

url1="http://127.0.0.1:8000/nasa/"
url = "http://127.0.0.1:8000/pk/"
response = requests.get(url)

if response.status_code==200:
    data = response.json()
    # print(data)
    for item in data:
        
        print(item['unique_id'])
        if check_unique_id_exists(conn,item['unique_id']):
            print("id existed")
            for url_item in item['urls']:
                if url_item['camera_id'] is None:
                    # Generate a unique camera ID based on the URL
                    url = url_item['url']
                    camera_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
                    url_item['camera_id'] = camera_id
                    # print(camera_id,url)
    
                    updated_data = {
                        
                        'camera_id': camera_id,
                        'url':url
                    }
                    
                    # # Send the updated data back using a PUT request
                    put_response = requests.put(url1, json=updated_data)
                    print("update send")
                    
                    if put_response.status_code == 200:
                        print("Data updated successfully")
                    else:
                        print("Failed to update data")
            update_urls(conn,item['unique_id'],item['urls'])
        else:
            continue
            
    
else:
    print("Failed to fetch data from the server")






















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
    # shutil.rmtree(extract_dir)

    print("all_images folder deleted.")

extract_dir = "/Users/prerak/Desktop/new approach/apicreator2/all_images"  # Path to the directory containing folders of images
encoder_dir = "/Users/prerak/Desktop/new approach/apicreator2/encodings"  # Directory to save the encoded faces

all_images_dir = "/Users/prerak/Desktop/new approach/apicreator2/all_images"
os.makedirs(all_images_dir, exist_ok=True)

# Get data from Firebase
def get_data_all_unique_id(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM all_unique_ids")
        
        data = {}
        for row in cursor.fetchall():
            unique_id, urls = row[0], row[1]
            # print(unique_id)
            data[unique_id] = {'urls': urls}
        cursor.close()
        return data
    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving data from PostgreSQL", error)
        return {}
data=get_data_all_unique_id(conn)
print(data)





# Process the data
for unique_id, value in data.items():
    urls_list = value.get('urls', [])
    for url_item in urls_list:
        camera_id = url_item.get('camera_id')
        images = url_item.get('images', [])
        for image_details in images:
            image_url = image_details.get('image_url')
            image_name = image_details.get('image_name')
            image_path = download_and_store_image(image_url, camera_id, image_name)
            if image_path:
                print(f"Image saved at: {image_path}")

# # Encode faces
encode_faces(extract_dir, encoder_dir)









# Process the data
# for unique_id, value in data.items():
#     urls = value.get('urls', {})
#     for camera_id, details in urls.items():
#         images = details.get('images', [])
#         for image_details in images:
#             image_url = image_details.get('image_url')
#             image_name = image_details.get('image_name')
#             image_path = download_and_store_image(image_url, camera_id, image_name)
#             if image_path:
#                 print(f"Image saved at: {image_path}")


