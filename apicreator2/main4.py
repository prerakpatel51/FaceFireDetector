import pickle
import cv2
import mediapipe as mp
import face_recognition
import cvzone
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import psycopg2
# from encoder3 import encode_faces


def x(camera_id,url,encoder_name):


    def create_table_if_not_exists(conn):
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS known_log (
                id SERIAL PRIMARY KEY,
                camera_id VARCHAR(255),
                name VARCHAR(255),
                time TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()

        
        
    def create_unknown_faces_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unknown_log (
                    id SERIAL PRIMARY KEY,
                    camera_id VARCHAR(255),
                    image_name VARCHAR(255),
                    
                    image_data BYTEA,
                    detection_time TIMESTAMP
                )
            """)
            conn.commit()
            print(f"Table {camera_id}_unknown_faces created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error creating table:", error)
        finally:
            if cursor:
                cursor.close()    
        
        
        
        
        
    def insert_detection_event(conn, camera_id,name ):
        cursor = conn.cursor()
        current_time = datetime.now()
        cursor.execute("""
            INSERT INTO known_log (camera_id,name, time)
            VALUES (%s, %s, %s)
        """, (camera_id,name, current_time))
        print("known person saved to log")
        conn.commit()
        cursor.close()

    def insert_unknown_face(conn,camera_id ,image_name, image_data, detection_time):
        try:
            cursor = conn.cursor()
            image_data=cv2.cvtColor(image_data,cv2.COLOR_BGR2RGB)
            # Convert the image data to binary format (BYTEA)
            image_data_bytes = cv2.imencode('.jpg', image_data)[1].tobytes()
            
            cursor.execute("""
                INSERT INTO unknown_log(camera_id, image_name, image_data, detection_time)
                VALUES (%s, %s, %s,%s)
            """, (camera_id,image_name, image_data_bytes, detection_time))
            conn.commit()
            print("Unknown person saved to database")
        except (Exception, psycopg2.Error) as error:
            print("Error inserting unknown face:", error)
        finally:
            if cursor:
                cursor.close()


    conn = psycopg2.connect(
            dbname='face',
            user='face',
            password='root',
            host='localhost',
            port=5432,
    )

    create_table_if_not_exists(conn)
    create_unknown_faces_table(conn)


    cap = cv2.VideoCapture(0)
    cap.set(3,480)
    cap.set(4,640)



    # loading the encoder file
    print("Loading Encoding File")
    file = open(encoder_name, 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, empIds = encodeListKnownWithIds

    print("Loaded Encode file")
    print(empIds)
    personlist = []
    counter = 0
    threshold = 50
   




    while True:
            
            
                success, img = cap.read()

                imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img.flags.writeable = False
                
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                lmList = []

                faceCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)


                known_face_detected = False
                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                    matchIndex = np.argmin(faceDis)

                    
                    
                    if matches[matchIndex]:
                        # print("Known face Detected through search Database::::", empIds[matchIndex])
                        known_face_detected = True
                      
                        
                        if counter % threshold == 0:
                            personlist.append(empIds[matchIndex])
                            # print(empIds[matchIndex])
                            insert_detection_event(conn,camera_id,empIds[matchIndex])
                            print("known person saved to database")
                            counter=0
                            
                        
                        
                        
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
                        bbox = x1, y1, x2 - x1, y2 - y1
                        img = cvzone.cornerRect(img, bbox, rt=0)
            
                if not known_face_detected and len(faceCurFrame) > 0:
                    
                   
                    if counter % threshold == 0:
                            personlist.append("unknown person")
                            insert_detection_event(conn,camera_id,'Unknown Person')
                            
                            insert_unknown_face(conn,camera_id ,'Unknown Person', imgS, datetime.now())
                           
                            counter=0
                            
               
                counter += 1
              

    cap.release()
    cv2.destroyAllWindows()            


        # Close the connection
    conn.close()









