from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from django.shortcuts import render
from .forms import *
from django.utils import timezone


def test1(request):
    return HttpResponse("blog/test1 응답!")

def test2(request, no):
    print('no 타입:', type(no))
    return HttpResponse(f'no:{no}')

def test3(request, year, month, day):
    return HttpResponse(f'년:{year}, 월:{month}, 일:{day}')

def test4(request):
    return render(request, 'blog/test4.html', {'score':70})

def test5(request):
    var ='''
    Miracles happen to only those who believe in them.
    Think like a man of action and act like man of thought.
    Courage is very important. Like a muscle, it is strengthened by use.
    Life is the art of drawing sufficient conclusions from insufficient premises.
    By doubting we come at the truth.
    A man that has no virtue in himself, ever envies virtue in others.
    When money speaks, the truth keeps silent.
    Better the last smile than the first laughter.
    '''
    return render(request, 'blog/test5.html', {'var':var})

def test6(request):
    d1 = timezone.now()
    d2 = timezone.datetime(2001,3,19)
    d3 = timezone.datetime(2030,3,19)
    return render(request, 'blog/test6.html', {'date1':d1, 'date2':d2, 'date3':d3})


def test7(request):
    print('요청방식 : ', request.method)
    print('GET방식으로 전달된 질의 문자열 :', request.GET)
    print('Post방식으로 전달된 질의 문자열 :', request.POST)
    print('업로드 파일 : ', request.FILES)
    return render(request, 'blog/form_test.html')


def list(request):
    post_list = Post.objects.all()
    return HttpResponse(post_list)


def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return HttpResponse(post.title)
