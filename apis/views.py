from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserSerializer, MovieSerializer, RatingsSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from . models import User, Movie, Ratings
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        Token.objects.filter(user=user).delete()
        if user:
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
            "token": token.key,
            "data": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "password": user.password,
                "phone": user.phone
            },
            "success": True,
            "message": "Success",
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogout(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)


# class AddMovieAPIView(generics.CreateAPIView):
#     serializer_class = MovieSerializer

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class MovieListAPIView(generics.ListAPIView):
#     serializer_class = MovieSerializer

#     def get_queryset(self):
#         user = self.request.user
#         query = self.request.query_params.get('name', None)
        
#         if query:
#             queryset = Movie.objects.filter(
#                 user=user,
#                 name__icontains=query
#             )
#         else:
#             queryset = Movie.objects.filter(user=user)
        
#         for movie in queryset:
#             average_rating = Ratings.objects.filter(movie_id=movie).aggregate(Avg('rating'))['rating__avg']
#             movie.average_rating = average_rating
        
#         return queryset

# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer

#     def get_queryset(self):
#         user = self.request.user
#         query = self.request.query_params.get('name', None)
        
#         if query:
#             queryset = Movie.objects.filter(
#                 user=user,
#                 name__icontains=query
#             )
#         else:
#             queryset = Movie.objects.filter(user=user)
        
#         for movie in queryset:
#             average_rating = Ratings.objects.filter(movie_id=movie).aggregate(Avg('rating'))['rating__avg']
#             movie.average_rating = average_rating
        
#         return queryset
    
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # Set the user before saving
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('name', None)
        
        if query:
            queryset = Movie.objects.filter(
                user=user,
                name__icontains=query
            )
        else:
            queryset = Movie.objects.filter(user=user)
        
        for movie in queryset:
            average_rating = Ratings.objects.filter(movie_id=movie).aggregate(Avg('rating'))['rating__avg']
            movie.average_rating = average_rating
        
        return queryset

class RatingsViewSet(viewsets.ModelViewSet):
    serializer_class = RatingsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Ratings.objects.none()

    def get_queryset(self):
        user = self.request.user
        return Ratings.objects.filter(movie_id__user=user)