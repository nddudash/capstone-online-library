from django.shortcuts import render
from book.models import Book

# Create your views here.


def BookList_view(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})