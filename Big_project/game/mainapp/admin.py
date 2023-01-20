from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Item)
admin.site.register(Shop)
admin.site.register(Character)
admin.site.register(HavingItem)
admin.site.register(wearing)
admin.site.register(Skill)
admin.site.register(CharacterSkill)


# ItemImage 클래스를 inline으로 나타낸다.
class ItemImageInline(admin.TabularInline):
    model = ItemImage

# Item 클래스는 해당하는 ItemImage 객체를 리스트로 관리하는 한다. 
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline, ]

# Register your models here.
admin.site.register(Item, ItemAdmin)