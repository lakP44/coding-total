from django.urls import path, include
from rest_framework import routers
from api2.views import *

# Routers provide an easy way of automatically determining the URL conf.

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),   
    path('post/', PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-detail'),
    path('comment/', CommentCreateAPIView.as_view(), name='comment-list'),
    path('post/<int:pk>/like/', PostLikeAPIView.as_view(), name="post-like"),
    path('catetag/', CateTagAPIView.as_view(), name='cateTag' ),
    
]