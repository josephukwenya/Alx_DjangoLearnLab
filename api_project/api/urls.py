from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

router.register(r'book_all', BookViewSet, basename='book_all')

urlpatterns = [
  path('books/', BookList.as_view(), name='book-list'),
  path('auth-token/', obtain_auth_token, name='api_token_auth'),
  path('', include(router.urls)),
]