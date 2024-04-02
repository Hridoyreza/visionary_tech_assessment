from . models import *
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','phone','email']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','phone', 'password', 'email']


class MovieSerializer(serializers.ModelSerializer):
    release_date = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y'])
    average_rating = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = Movie
        fields = ['id','name', 'genre', 'rating', 'release_date', 'average_rating']


class RatingsSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model= Ratings
        fields = ['id', 'user_id', 'movie_id', 'rating']
    
    def get_user_id(self, obj):
        if obj.movie_id:
            return obj.movie_id.user_id
        return None