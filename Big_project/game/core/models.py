# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    last_logout = models.DateTimeField(blank=True, null=True)
    time_per_day = models.IntegerField(default=0)
    time_total = models.IntegerField(default=0)
    age = models.CharField(max_length=3, blank=True, null=True)
    gender = models.CharField(max_length=2, blank=True, null=True)
    money = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile', default="profile/default.png")

class Beautyproduct(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey('Brand', models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    effect = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'beautyproduct'

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'brand'

    def __str__(self):
        return self.name


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, models.CASCADE)
    discount_rate = models.CharField(max_length=255)

    class Meta:
        db_table = 'coupon'

class MonsterAbility(models.Model):
    id = models.AutoField(primary_key=True)
    abilityName = models.CharField(max_length=255)
    abilityType = models.CharField(max_length=255)
    class Meta:
        db_table = 'monster_ability'
    def __str__(self):
        return self.abilityName        
        
class Monster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    hp = models.IntegerField()
    skills = models.ForeignKey(MonsterAbility, models.CASCADE)
    mob_type = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'monster'
        
class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    achieveName = models.CharField(max_length=255)
    achieve = models.CharField(max_length=255)
    achieveImage = models.ImageField(upload_to='acievement', default="default.png")
    
    owner = models.ManyToManyField(User, through='AchieveUser')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.achieveName
    
class AchieveUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achieve = models.ForeignKey(Achievement,on_delete=models.CASCADE)
    achieveGet = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class HistoryByDay(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    face_image = models.ImageField(upload_to='face')
    age = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    mouthCnt = models.IntegerField(default=0)
    eyeCnt = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username + '/' + str(self.date)

class FacePoint(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    time = models.DateTimeField(auto_created=True)
    x_0 = models.FloatField()
    y_0 = models.FloatField()
    x_1 = models.FloatField()
    y_1 = models.FloatField()
    x_2 = models.FloatField()
    y_2 = models.FloatField()
    x_3 = models.FloatField()
    y_3 = models.FloatField()
    x_4 = models.FloatField()
    y_4 = models.FloatField()
    x_5 = models.FloatField()
    y_5 = models.FloatField()
    x_6 = models.FloatField()
    y_6 = models.FloatField()
    x_7 = models.FloatField()
    y_7 = models.FloatField()
    x_8 = models.FloatField()
    y_8 = models.FloatField()
    x_9 = models.FloatField()
    y_9 = models.FloatField()
    x_10 = models.FloatField()
    y_10 = models.FloatField()
    x_11 = models.FloatField()
    y_11 = models.FloatField()
    x_12 = models.FloatField()
    y_12 = models.FloatField()
    x_13 = models.FloatField()
    y_13 = models.FloatField()
    x_14 = models.FloatField()
    y_14 = models.FloatField()
    x_15 = models.FloatField()
    y_15 = models.FloatField()
    x_16 = models.FloatField()
    y_16 = models.FloatField()
    x_17 = models.FloatField()
    y_17 = models.FloatField()
    x_18 = models.FloatField()
    y_18 = models.FloatField()
    x_19 = models.FloatField()
    y_19 = models.FloatField()
    x_20 = models.FloatField()
    y_20 = models.FloatField()
    x_21 = models.FloatField()
    y_21 = models.FloatField()
    x_22 = models.FloatField()
    y_22 = models.FloatField()
    x_23 = models.FloatField()
    y_23 = models.FloatField()
    x_24 = models.FloatField()
    y_24 = models.FloatField()
    x_25 = models.FloatField()
    y_25 = models.FloatField()
    x_26 = models.FloatField()
    y_26 = models.FloatField()
    x_27 = models.FloatField()
    y_27 = models.FloatField()
    x_28 = models.FloatField()
    y_28 = models.FloatField()
    x_29 = models.FloatField()
    y_29 = models.FloatField()
    x_30 = models.FloatField()
    y_30 = models.FloatField()
    x_31 = models.FloatField()
    y_31 = models.FloatField()
    x_32 = models.FloatField()
    y_32 = models.FloatField()
    x_33 = models.FloatField()
    y_33 = models.FloatField()
    x_34 = models.FloatField()
    y_34 = models.FloatField()
    x_35 = models.FloatField()
    y_35 = models.FloatField()
    x_36 = models.FloatField()
    y_36 = models.FloatField()
    x_37 = models.FloatField()
    y_37 = models.FloatField()
    x_38 = models.FloatField()
    y_38 = models.FloatField()
    x_39 = models.FloatField()
    y_39 = models.FloatField()
    x_40 = models.FloatField()
    y_40 = models.FloatField()
    x_41 = models.FloatField()
    y_41 = models.FloatField()
    x_42 = models.FloatField()
    y_42 = models.FloatField()
    x_43 = models.FloatField()
    y_43 = models.FloatField()
    x_44 = models.FloatField()
    y_44 = models.FloatField()
    x_45 = models.FloatField()
    y_45 = models.FloatField()
    x_46 = models.FloatField()
    y_46 = models.FloatField()
    x_47 = models.FloatField()
    y_47 = models.FloatField()
    x_48 = models.FloatField()
    y_48 = models.FloatField()
    x_49 = models.FloatField()
    y_49 = models.FloatField()
    x_50 = models.FloatField()
    y_50 = models.FloatField()
    x_51 = models.FloatField()
    y_51 = models.FloatField()
    x_52 = models.FloatField()
    y_52 = models.FloatField()
    x_53 = models.FloatField()
    y_53 = models.FloatField()
    x_54 = models.FloatField()
    y_54 = models.FloatField()
    x_55 = models.FloatField()
    y_55 = models.FloatField()
    x_56 = models.FloatField()
    y_56 = models.FloatField()
    x_57 = models.FloatField()
    y_57 = models.FloatField()
    x_58 = models.FloatField()
    y_58 = models.FloatField()
    x_59 = models.FloatField()
    y_59 = models.FloatField()
    x_60 = models.FloatField()
    y_60 = models.FloatField()
