
from django.urls import path, include
from . import views


urlpatterns = [
    path('test1/', views.test1),
    path('test2/<int:no>/', views.test2),
    path('test3/<year>/<month>/<day>/', views.test3),
    path('test4/', views.test4),
    path('test5/', views.test5),
    path('test6/', views.test6),
    path('test7/', views.test7),

    path('', views.list),
    path('<int:id>/', views.detail),


]
