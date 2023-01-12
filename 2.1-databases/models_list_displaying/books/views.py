from books.models import Book
from django.shortcuts import render, redirect


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    all_books = Book.objects.all()
    context = {'all_books': all_books}
    return render(request, template, context)


def book_date(request, pub_date):
    books_by_date = Book.objects.filter(pub_date=pub_date)
    try:
        next_page = books_by_date[len(books_by_date)-1].get_next_by_pub_date()
    except Book.DoesNotExist:
        next_page = None
    try:
        prev_page = books_by_date[0].get_previous_by_pub_date()
    except Book.DoesNotExist:
        prev_page = None
    context = {'books_by_date': books_by_date, 'next_page': next_page, 'prev_page': prev_page}
    return render(request, 'books/book_date.html', context)
