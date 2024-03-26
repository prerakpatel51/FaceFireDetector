import psycopg2,base64
from psycopg2 import sql
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
def retrieve_log_from_db(camera_id):
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname="face",
        user="face",
        password="root",
        host="localhost",
        port="5432"
    )

    # Create a cursor object
    cur = conn.cursor()

    # Define the start and end timestamps
    start_timestamp = "2024-03-11 11:01:50.696038"
    end_timestamp = "2024-03-11 12:20:00.0000"

    # Define the camera_id
    camera_id = "1062b7aa-71e5-5261-9b96-3b0d1fc85cc9"

    # Execute a query to retrieve names for the specified camera_id and time range
    query = sql.SQL("SELECT name,time FROM known_log WHERE time BETWEEN %s AND %s AND camera_id = %s;")
    cur.execute(query, (start_timestamp, end_timestamp, camera_id))

    

    # Fetch all rows
    rows = cur.fetchall()
    #  Create a list to store the results
    known_result_list = []
    for row in rows:
        known_result_list.append({"name": row[0], "time": str(row[1])})
    import json
    # Convert the list to a JSON string
    known_result_json = json.dumps(known_result_list)
    # print(known_result_json)
    
    
    
    unknown_result_list=[]
    query=sql.SQL("SELECT image_name,detection_time,image_data FROM unknown_log where detection_time BETWEEN %s AND %s and camera_id = %s;")
    cur.execute(query,(start_timestamp,end_timestamp,camera_id))
    rows=cur.fetchall()
    for row in rows:
        unknown_result_list.append({"name":row[0],"time":str(row[1]),"image_data":row[2].tobytes()})
        # image = Image.open(BytesIO(row[2]))
        

# Convert the binary data to an image
       

# Convert the image to RGB if it's not already in RGB format
        image = Image.open(BytesIO(row[2].tobytes()))
        plt.imshow(image)
        plt.axis('off')  # Turn off axis numbers
        plt.show()
    # print(unknown_result_list)
    # Close the cursor and the connection
    cur.close()
    conn.close()
    
    
retrieve_log_from_db("wfewrfref")