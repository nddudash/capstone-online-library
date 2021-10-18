from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from book.models import Book
from custom_user.models import CustomUser
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def reservation_view(request, id):
    user = CustomUser.objects.get(username=request.user.username)
    book = Book.objects.get(id=id)

    if book not in user.checked_out_books.all():
        user.reserved_books.add(book)
        user.save()
        book.is_reserved = True
        book.reserved_by = user
        book.save()
        return HttpResponseRedirect(reverse('books_page'))

@login_required
def remove_reservation_view(request, id):
    user = CustomUser.objects.get(username=request.user.username)
    book = Book.objects.get(id=id)

    if book in user.reserved_books.all():
        user.reserved_books.remove(book)
        user.save()
        return HttpResponseRedirect(reverse('books_page'))
