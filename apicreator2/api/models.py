from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    unique_id = models.CharField(max_length=200, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name
    
    

class URL(models.Model):
    user = models.ForeignKey(User, related_name='urls', on_delete=models.CASCADE)
    url = models.URLField()
    camera_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.url


class Image(models.Model):
    url = models.ForeignKey(URL, related_name='images', on_delete=models.CASCADE)
    image_name=models.CharField(max_length=300,null=True)
    image = models.ImageField(upload_to='images/')
    

    def __str__(self):
        return str(self.image)
    
    
