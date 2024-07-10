import cv2
import numpy as np
import psycopg2
from datetime import datetime
import time
def motion(url,camera_id):
      
    def insert_motion_detected(conn,camera_id , image_data, detection_time):
            try:
                cursor = conn.cursor()
                
                # image_data=cv2.cvtColor(image_data,cv2.COLOR_BGR2RGB)
                # Convert the image data to binary format (BYTEA)
                image_data_bytes = cv2.imencode('.jpg', image_data)[1].tobytes()
                
                cursor.execute("""
                    INSERT INTO app1_motion_log(camera_id,image_data, detection_time)
                    VALUES (%s, %s, %s)
                """, (camera_id, image_data_bytes, detection_time))
                conn.commit()
                print("Motion detected and Saved to database")
            except (Exception, psycopg2.Error) as error:
                print("Error: Inserting in db error", error)
            finally:
                if cursor:
                    cursor.close()



    conn = psycopg2.connect(
                dbname='finalapi',
                user='finalapi',
                password='root',
                host='localhost',
                port=5432,
        )
       
    
    
    
    cap = cv2.VideoCapture(0)
    ret, img1 = cap.read()
    ret, img2 = cap.read()
    
    counter=0

    while cap.isOpened():
        img1_resized = cv2.resize(img1, (640, 640))  # Replace width and height with desired dimensions
        img2_resized = cv2.resize(img2, (640, 640))

        diff = cv2.absdiff(img1_resized, img2_resized)
        
        # diff = cv2.absdiff(img1, img2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        
        dilated = cv2.dilate(thresh, (4,4), iterations=1)
    
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 1100:
                continue
            cv2.rectangle(img1, (x, y), (x+w, y+h), (255, 255, 0), 2)
            
            cv2.putText(img1, "{}".format('Alert: Motion detected'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 255), 3)
            if counter % 60 == 0:
                    # Insert into database
                insert_motion_detected(conn, camera_id=camera_id, image_data=img1, detection_time=datetime.now())
            counter -= 40

        counter += 1
            
        # cv2.imshow("dilated", dilated)
        # cv2.imshow("feed", img1)
        # cv2.imshow("thresh", thresh)
        
        img1 = img2
        ret, img2 = cap.read()

        cv2.waitKey(20)
            
    cv2.destroyAllWindows()
    cap.release()






