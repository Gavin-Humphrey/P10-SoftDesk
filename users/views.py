from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class SignupView(viewsets.ModelViewSet):

    """
    UserModel View.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
