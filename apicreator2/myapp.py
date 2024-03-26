import requests
import uuid,json
# [{'name': 'Prerak Patel', 'email': 'patel.ketan51002@gmail.com', 'unique_id': None}]



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
    
   
    
        
    
    
    
    
    
    
    
# import requests
# import uuid
url1="http://127.0.0.1:8000/nasa/"
url = "http://127.0.0.1:8000/pk/"
response = requests.get(url)

if response.status_code==200:
    data = response.json()
    print(data)
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






