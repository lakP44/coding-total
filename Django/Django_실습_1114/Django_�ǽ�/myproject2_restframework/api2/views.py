from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api2.serializers import *
from blog.models import *

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
