# from rest_framework import serializers
# from .models import User
# class User_serializers(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField()
#     unique_id = serializers.CharField(max_length=200)


from rest_framework import serializers
from .models import User

class User1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'unique_id']


from rest_framework import serializers
from .models import User, URL, Image

class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_name=serializers.CharField(max_length=300)
    class Meta:
        model = Image
        fields = ['image_url','image_name']

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

class URLSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = URL
        fields = ['url', 'camera_id', 'images']

class UserSerializer(serializers.ModelSerializer):
    urls = URLSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['unique_id', 'urls']
