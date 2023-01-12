
from django.contrib import admin
from django.urls import path

from books.views import books_view, index, book_date

urlpatterns = [
    path('', index, name='index'),
    path('books/', books_view, name='books'),
    path('books/<pub_date>/', book_date, name='book_date'),
    path('admin/', admin.site.urls),
]
