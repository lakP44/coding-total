from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):
    class TypeChoices(models.TextChoices):
        HELMET = "헬멧",
        HAIR = "머리",
        FACE = "얼굴",
        TOP = "상의",
        BOTTOM = "하의",
        SHOE = "신발",
        WEAPON = "무기",
        SHIELD = "방패"


    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(choices=TypeChoices.choices, max_length=2)
    # level = models.IntegerField(default=1, validators=[
    #     MinValueValidator(1),
    #     MaxValueValidator(999)
    # ])

    def __str__(self):
        return self.name

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class Shop(models.Model):
  item = models.ForeignKey("Item", related_name='history', on_delete = models.CASCADE)
  pay = models.IntegerField(default=0)
  quantity = models.IntegerField(null=True, blank=True) # 생략 가능. 생략하면 무제한 판매 

  def __str__(self):
    return self.item.name


class Character(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey("core.user", models.CASCADE)
  level = models.IntegerField(default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(999)
    ])
  # hp = models.
  exp = models.IntegerField()

  def __str__(self):
    return self.user.username
  
class HavingItem(models.Model) :
  userID = models.ForeignKey('core.user', models.CASCADE)
  itemID = models.ForeignKey('Item', models.CASCADE)
  
  def __str__(self):
    return self.itemID.name
  
class wearing(models.Model):
  id = models.AutoField(primary_key=True)
  character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
  havingItem = models.ForeignKey(HavingItem, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return self.havingItem.itemID.name

class Skill(models.Model):
  class TypeChoices(models.TextChoices):
    water = "물",
    fire = "불",
    grass = "풀"

  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=255)
  type = models.CharField(choices=TypeChoices.choices, max_length=2)
  damage = models.IntegerField(null=True)

  def __str__(self):
        return self.name


class CharacterSkill(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)

  def __str__(self):
        return self.skill.name

