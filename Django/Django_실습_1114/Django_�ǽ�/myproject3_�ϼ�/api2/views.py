from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

from django.contrib.auth.models import User
from api2.serializers import *
from blog.models import *

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostPageNumberPagination(PageNumberPagination):
    page_size = 3
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number ),
        ]))    

# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     pagination_class = PostPageNumberPagination
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }    


# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostRetrieveSerializer

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = {'like':instance.like+1}
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data['like'])    


class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()
        data = {
            'cateList' :cateList,
            'tagList' : tagList
        }    

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)


class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        return Response(instance.like)

def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_update_dt()
    except instance.DoesNotExist:
        prev = None
    try:
        next_= instance.get_next_by_update_dt()
    except instance.DoesNotExist:
        next_= None
    
    return prev, next_


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()
        data = {
            'post': instance,
            'prevPost' : prevInstance,
            'nextPost' : nextInstance,
            'commentList' : commentList
        }

        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)    
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }        

class PostListAPIView(ListAPIView):
    
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }    
    def get_queryset(self):
        paramCate = self.request.GET.get('category')
        paramTag = self.request.GET.get('tag')
        if paramCate:
            queryset = Post.objects.filter(category__name__iexact=paramCate)
        elif paramTag:
            queryset = Post.objects.filter(tags__name__iexact=paramTag)
        else:
            queryset = Post.objects.all()        

        return queryset
