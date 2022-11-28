from django.contrib.auth.models import User 
#from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer


class SignupView(viewsets.ModelViewSet):

    """
    UserModel View.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all() 



