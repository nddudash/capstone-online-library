from django.shortcuts import render

from book.models import Book

# Create your views here.
def book_detail(request,id):
  template_name = 'book_detail.html'
  book = Book.objects.get(id=id)
  context = {'book': book}
  return render(request, template_name, context)
