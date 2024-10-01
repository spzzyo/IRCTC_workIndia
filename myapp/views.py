from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import CustomUser
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny




class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == '1'

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_only_view(request):
    return Response({'message': 'Welcome, admin!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def general_view(request):
    return Response({'message': 'Welcome to the general view!'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def custom_user_login(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')

  
    user = authenticate(username=username_or_email, password=password)

    if user is None:
        try:
            user = CustomUser.objects.get(email=username_or_email)
            user = authenticate(username=user.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

    if user:
        token = AccessToken.for_user(user)
        token['user_type'] = user.user_type 
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)









@permission_classes([AllowAny])
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return 201 Created
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    


def signup_view(request):
    return render(request, 'signup.html')


def signin_view(request):
    return render(request, 'signin.html')



   
   

