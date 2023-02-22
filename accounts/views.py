from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import MyUser
from .serializers import UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)