from django.shortcuts import render, redirect
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from .serializers import *
from .serializers import ShopSerializer
import redis
import base64

import numpy as np
import tensorflow as tf
from PIL import Image

from .serializers import *
from core.models import User, HistoryByDay
from .serializers import *
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings


# Create your views here.
def main(request):
  return render(request, 'mainapp/main.html')

def store(request):
  return render(request, 'mainapp/store.html')

def dic(request):
  return render(request, 'mainapp/dic.html')

def achievement(request):
  return render(request, 'mainapp/achievement.html')

def character(request):
  return render(request, 'mainapp/character.html')

def skills(request):
  return render(request, 'mainapp/skills.html')

def analysis(request):
  return render(request, 'mainapp/analysis.html')

def recsys(request):
  return render(request, 'mainapp/recsys.html')

class shopAPI(APIView):
  def get(self, request):
    shop_list = Shop.objects.all()
    serializer = ShopSerializer(shop_list, many=True)
    return Response(serializer.data)
  
class ItemAPI(APIView):
  def get(self, request):
    Item_list = Item.objects.prefetch_related('history').all()
    serializer = ItemSerializer(Item_list, many=True)
    return Response(serializer.data)
  
class StoreAPI(APIView) :
  def post(self, request) :
    Post = StorePostSerializer(data=request.data)
    print('post 요청')
    print(Post)
    if Post.is_valid() :
      print('post alive')
      Post.save()
      return Response(Post.data)
    else :
      print('post dead')
      return Response(Post.data)
    
  def patch(self, request) :
    value = int(request.data.__getitem__('money'))
    data = request.user.money - value
    request.user.money = data
    request.user.save()
    return Response()
    
class HavingItemAPI(APIView):
  def get(self, request):
    HavingItem_list = HavingItem.objects.all()
    serializer = HavingItemSerializer(HavingItem_list, many=True)
    return Response(serializer.data)
  
class WearingItemAPI(APIView):
  def get(self, request):
    Wearing_list = wearing.objects.all()
    serializer = WearingSerializer(Wearing_list, many=True)
    return Response(serializer.data)
  
def result(request):
  left_eye_cnt = int(request.GET.get('left_eye', 0))
  right_eye_cnt = int(request.GET.get('right_eye', 0))
  mouth_cnt = int(request.GET.get('mouth', 0))

  # increase count 
  history =  HistoryByDay.objects.get(user = request.user, date = timezone.now().today())
  history.mouthCnt = history.mouthCnt + mouth_cnt
  history.eyeCnt = history.eyeCnt + left_eye_cnt + right_eye_cnt
  
  # age predict
  model = tf.keras.models.load_model(settings.AGE_MODEL_PATH)
  X = []
  width = 100
  height = 200
  image = Image.open(history.face_image.file)
  image = image.convert('RGB')
  image = image.resize((width, height))
  X.append(np.array(image))
  X = np.array(X)
  X = X.astype('float32')
  X /= 255.0
  age_predicted = int(model.predict(X))
  history.age = age_predicted

  history.save()

  return render(request, 'mainapp/result.html', {
    'age_predicted': age_predicted,
    'left_eye_cnt': left_eye_cnt,
    'right_eye_cnt': right_eye_cnt,
    'mouth_cnt': mouth_cnt,
    'face_image': history.face_image.url
  })

def find_room(request):
  return render(request, 'mainapp/find-room.html')

# 대기실
def wait_room(request, room_name):
  # 방 목록 저장 redis
  redis_client = redis.StrictRedis.from_url("rediss://red-cegkhc02i3mkhvoakgh0:Z6M9PSoaNV0aOv0XR2y3CmJ8TpYGGGfQ@singapore-redis.render.com:6379/10", encoding="utf-8", decode_responses=True)
  # 대기실에 들어오는 사람이 없으면 
  # redis_client.expire(room_name, 60 * 10) # 단위(초) - 10분 뒤에 방 삭제
  # redis_client.sadd(room_name, request.user.username)
  # players_in_room =  redis_client.smembers(room_name)
  # print(players_in_room)
  return render(request, 'mainapp/wait-room.html', {
    # 'players_in_room': players_in_room,
    'player_name': request.user.username,
    'room_name': room_name,
  })

def pvp(request, room_name):
  return render(request, 'mainapp/pvp.html', {
    'room_name': room_name,
    'player_name': request.user.username
  })

class FaceImageAPI(APIView):
  def post(self, request):
    # print(timezone.now().date())
    # 오늘의 History가 이미 있으면
    face_base64 = request.data.__getitem__('face')
    format, imgstr = face_base64.split(';base64,') 
    ext = format.split('/')[-1]
    today = timezone.now().today()
    face_image = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}-{today}.{ext}')
    history, created = HistoryByDay.objects.get_or_create(
      user  = request.user,
      date = today,
      defaults= {'face_image' : face_image}
    )

    if not created:
      history.face_image = face_image
      history.save()
    return Response()
