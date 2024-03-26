import psycopg2
import cv2
from io import BytesIO
import numpy as np
# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='finalapi',
    user='finalapi',
    password='root',
    host='localhost',
    port=5432,
)

# Create a cursor object using the connection
cursor = conn.cursor()

# Query to retrieve image data from the app1_fire_log table
cursor.execute("SELECT image_data FROM app1_fire_log")

# Fetch all rows containing image data
rows = cursor.fetchall()

# Loop through the rows and display images
for row in rows:
    # Read the image data as bytes
    image_data_bytes = row[0]

    # Convert the image data bytes to a numpy array
    image_data_np = np.frombuffer(image_data_bytes, np.uint8)

    # Decode the numpy array into an image
    image = cv2.imdecode(image_data_np, cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(1000)

# Close the cursor and connection
cursor.close()
conn.close()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
