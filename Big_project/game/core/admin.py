from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Beautyproduct)
admin.site.register(Brand)
admin.site.register(Coupon)
admin.site.register(Achievement)
admin.site.register(AchieveUser)
admin.site.register(HistoryByDay)