from django.urls import path, include
from . views import UserRegistration, UserLogin, UserLogout, UserListView, RatingsViewSet, MovieViewSet
#MovieListAPIView, AddMovieAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ratings', RatingsViewSet)

router_movies = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('users/', UserListView.as_view(), name='users'),
    path('logout/', UserLogout.as_view(), name='user_logout'),
    #path('add-movie/', AddMovieAPIView.as_view(), name='add-movie'),
    #path('movie-list/', MovieListAPIView.as_view(), name='movie-list'),
    #path('ratings/', AddRatingAPIView.as_view(), name='ratings'),
    path('', include(router.urls)),
]