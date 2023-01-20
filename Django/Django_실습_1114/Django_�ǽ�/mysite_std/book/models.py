from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)

    def __str__(self):
        return self.title   

    def get_absolute_url(self):
        return reverse('book:list')


# from book.models import Book
# for i in range(1, 11):
#     Book.objects.create(title=f'제목{i}', author=f'저자{i}', publisher=f'출판사{i}')
# Book.objects.count()  
