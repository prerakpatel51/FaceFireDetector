import psycopg2
import uuid
from multiprocessing import Process
import os
from main4 import x
def get_data_from_postgresql(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        data = {}
        for row in cursor.fetchall():
            unique_id, urls = row[0], row[1]
            data[unique_id] = {'urls': urls}
        cursor.close()
        print(data)
        return data
    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving data from PostgreSQL", error)
        return {}
def extract_camera_data(data):
    camera_data = {}
    for unique_id, value in data.items():
        urls_list = value.get('urls', [])
        for urls in urls_list:
            url = urls.get('url')
            camera_id = urls.get('camera_id')
            camera_data[camera_id] = url
    return camera_data

# def extract_camera_data(data):
#     camera_data = {}
#     for unique_id, value in data.items():
#         urls = value.get('urls', {})
#         for camera_id, details in urls.items():
#             url = details.get('url')
#             camera_data[camera_id] = url
#     return camera_data

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='face',
    user='face',
    password='root',
    host='localhost',
    port=5432
)

# Example usage
data = get_data_from_postgresql(conn, 'all_unique_ids')
if __name__=='__main__':
# Process the data
    for camera_id, url in extract_camera_data(data).items():
        print(f"Camera ID: {camera_id}, URL: {url}")

        encoder_name = f"/Users/prerak/Desktop/new approach/apicreator2/encodings/{camera_id}.pkl"
        if os.path.exists(encoder_name):
            p = Process(target=x, args=(camera_id, url, encoder_name))
            p.start()

    # Close the database connection
    conn.close()
