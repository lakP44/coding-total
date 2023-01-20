from rest_framework import serializers
from .models import *

class CurrentUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'profile_image', 'money', 'id']
    
class AchieveUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = AchieveUser
    fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
  class Meta:
    model = Achievement
    fields = '__all__'