from ultralytics import YOLO
import cv2
import math
import psycopg2
from datetime import datetime

def fire(camera_id,url):

    def insert_fire_detected(conn,camera_id , image_data, detection_time):
            try:
                cursor = conn.cursor()
                
                # image_data=cv2.cvtColor(image_data,cv2.COLOR_BGR2RGB)
                # Convert the image data to binary format (BYTEA)
                image_data_bytes = cv2.imencode('.jpg', image_data)[1].tobytes()
                
                cursor.execute("""
                    INSERT INTO app1_fire_log(camera_id,image_data, detection_time)
                    VALUES (%s, %s, %s)
                """, (camera_id, image_data_bytes, detection_time))
                conn.commit()
                print("Fire detected and Saved to database")
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



    # Running real time from webcam
    cap = cv2.VideoCapture('api/vid.mp4')
    model = YOLO('api/augmentedtwoclass73.pt')

    # Reading the classes
    classnames = ['Fire','Fire']

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        result = model(frame, stream=True)

        # Getting bbox, confidence, and class names information to work with
        for info in result:
            boxes = info.boxes

            for box in boxes:
                for i in range(len(box.cls)):
                    confidence = box.conf[i]
                    confidence = math.ceil(confidence * 100)
                    Class = int(box.cls[i])
                    if confidence > 45:
                        x1, y1, x2, y2 = box.xyxy[i]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 5)
                        if Class < len(classnames):
                            class_label = classnames[Class]
                        else:
                            class_label = f'Class {Class}'
                        cv2.putText(frame, f'{class_label} {confidence}%', (x1 + 8, y1 + 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        print(f'{class_label} detected with {confidence}% confidence')
                        insert_fire_detected(conn, camera_id=camera_id, image_data=frame, detection_time=datetime.now())

        # cv2.imshow('frame', frame)
        cv2.waitKey(1)
