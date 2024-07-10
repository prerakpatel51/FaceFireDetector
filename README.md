
# RTSP Based Camera Management and Monitoring System Using Python and Django
## Developed By Prerak Patel

This Django project provides a RESTful API for managing cameras, user IDs, and various detection processes including face detection, fire detection, and motion detection. It leverages Django ORM for data persistence and multiprocessing for concurrent task execution.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/prerakpatel51/FaceFireDetector.git
   cd finalapiwithfireandmotion
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Endpoints

### 1. Create User ID

**Endpoint:** `/create_user_id/`

**Method:** POST

**Parameters:**
- `name`: Name of the user (string)
- `email`: Email of the user (string)

**Response:**
- `user_id`: Unique ID generated for the user (string)

### 2. Create Camera ID

**Endpoint:** `/create_camera_id/`

**Method:** POST

**Parameters:**
- `user_id`: ID of the user for whom the camera ID is being created (string)

**Response:**
- `camera_id`: Unique ID generated for the camera (UUID)

### 3. Upload Images and URL for Face Detection

**Endpoint:** `/upload_imagesurl_and_url_face_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)
- `url`: URL associated with the camera feed (string)
- `image_urls`: JSON array of image URLs for face detection (string)
-  Use the apicreator2 to create an url for image a simple django webapp  

**Response:**
- `message`: Confirmation message (string)

### 4. Start Face Detection Process

**Endpoint:** `/start_camera_face_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)

**Response:**
- `message`: Confirmation message (string)

### 5. Stop Face Detection Process

**Endpoint:** `/stop_camera_face_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)

**Response:**
- `message`: Confirmation message (string)

### 6. Get Logs

**Endpoint:** `/getlog/`

**Method:** GET

**Parameters:**
- `user_id`: ID of the user (string)
- Optional:
  - `start_time`: Start time for log retrieval (datetime)
  - `end_time`: End time for log retrieval (datetime)

**Response:**
- `known_logs`: List of known logs (array of objects)
- `unknown_logs`: List of unknown logs (array of objects)

### 7. Upload URL for Fire Detection

**Endpoint:** `/upload_url_fire_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)
- `url`: URL associated with the fire detection service (string)

**Response:**
- `message`: Confirmation message (string)

### 8. Start Fire Detection Process

**Endpoint:** `/start_camera_fire_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)

**Response:**
- `message`: Confirmation message (string)

### 9. Stop Fire Detection Process

**Endpoint:** `/stop_camera_fire_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)

**Response:**
- `message`: Confirmation message (string)

### 10. Upload URL for Motion Detection

**Endpoint:** `/upload_url_motion_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)
- `url`: URL associated with the motion detection service (string)

**Response:**
- `message`: Confirmation message (string)

### 11. Start Motion Detection Process

**Endpoint:** `/start_camera_motion_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)

**Response:**
- `message`: Confirmation message (string)

### 12. Stop Motion Detection Process

**Endpoint:** `/stop_camera_motion_detection/`

**Method:** POST

**Parameters:**
- `camera_id`: ID of the camera (string)

**Response:**
- `message`: Confirmation message (string)

## Webhooks

This system supports webhooks for certain events like detection of motion and fire. Configure your webhook endpoint to receive POST requests with JSON payloads containing relevant information of the event

## Output Examples

### Fire Detection Output

<img width="627" alt="Screenshot 2024-04-05 at 5 29 25 PM" src="https://github.com/prerakpatel51/FaceFireDetector/assets/155515142/8c122187-f6cc-40a9-b3ca-6d6a08780d4f">
<img width="637" alt="Screenshot 2024-04-05 at 5 27 02 PM" src="https://github.com/prerakpatel51/FaceFireDetector/assets/155515142/d3a24303-2a19-4ae6-b25b-77c63df7fa95">


### Motion Detection Output
<img width="1728" alt="Screenshot 2024-04-09 at 10 28 16 AM 1" src="https://github.com/prerakpatel51/FaceFireDetector/assets/155515142/71562e77-1a74-40aa-acd4-52d6566d3b4d">


### Face Detection Output
<img width="650" height='500' alt="Screenshot 2024-04-09 at 10 28 16 AM 1" src="https://github.com/prerakpatel51/FaceFireDetector/assets/155515142/4d2da292-0f7a-4059-9195-3936f138c87d">
<img width="650" height='500' alt="Screenshot 2024-04-09 at 10 28 16 AM 1" src="https://github.com/prerakpatel51/FaceFireDetector/assets/155515142/f8bdbbd0-e144-495c-85b8-d8eabd4cf9b3">







## Developed By Prerak Patel

