from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, UpdateUserSerializer

# Create your views here.
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # create token and return it with user data
        user = User.objects.get(username=response.data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'user': response.data,
            'token': token.key,
        }
        return Response(data)

# Option 1: use default ObtainAuthToken but extend to return user info
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        user_data = UserSerializer(user).data
        return Response({'token': token.key, 'user': user_data})

# Profile view
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Follow / unfollow endpoints (simple)
from rest_framework import status

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            target = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail':'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if target == user:
            return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if user in target.followers.all():
            # unfollow
            target.followers.remove(user)
            action = 'unfollowed'
        else:
            target.followers.add(user)
            action = 'followed'

        return Response({'detail': f'{action} {target.username}'})