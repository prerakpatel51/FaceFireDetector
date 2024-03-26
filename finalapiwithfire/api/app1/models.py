from django.db import models



class User_Id(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user_id = models.CharField(max_length=200, unique=True)
    

class Camera_Id(models.Model):
    user_id = models.CharField(max_length=200)
    camera_id = models.CharField(max_length=200, unique=True)




class UploadUrlAndImages(models.Model):
    camera_id = models.CharField(max_length=200)
    url = models.URLField()
    image_urls = models.CharField(max_length=500)
    
    
    
    
class Status_Process(models.Model):
    process_id=models.CharField(max_length=300)
    camera_id=models.CharField(max_length=300)
    status=models.BooleanField()
    detection_type=models.CharField(max_length=200,default='None')
    
    
    

class KnownLog(models.Model):
    camera_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'known_log'
    

class UnknownLog(models.Model):
    camera_id = models.CharField(max_length=255, blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True, null=True)
    image_data = models.BinaryField(blank=True, null=True)
    detection_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unknown_log'
        
        
class Fire_Log(models.Model):
    camera_id = models.CharField(max_length=255, blank=True, null=True)
    detection_time = models.DateTimeField(blank=True, null=True)
    image_data = models.BinaryField(blank=True, null=True)
    


class UploadUrlFireDetection(models.Model):
    camera_id = models.CharField(max_length=200)
    url = models.URLField()
   
    
    

        
        
