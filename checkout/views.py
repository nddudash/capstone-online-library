from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from custom_user.models import CustomUser
from book.models import Book
from notification.models import Notifications


@login_required
def checkout_book_view(request, book_id):
    checkout_user = CustomUser.objects.get(username=request.user.username)
    book = Book.objects.get(id=book_id)

    if book.copies_available and not book in checkout_user.checked_out_books.all():
        book.copies_available += -1
        book.save()
        checkout_user.checked_out_books.add(book)
        checkout_user.save()
        return HttpResponseRedirect(reverse('book_detail_page', kwargs={'id': book_id}))

@login_required
def return_book_view(request, book_id):
    checkout_user = CustomUser.objects.get(username=request.user.username)
    book = Book.objects.get(id=book_id)

    if book in checkout_user.checked_out_books.all():
        if book.is_reserved:
            notification = Notifications.objects.create(
                user= book.customuser_set.first(),
                book= book,
                exclamation= True,
            )
            notification.save()
        book.copies_available += 1
        book.save()
        checkout_user.checked_out_books.remove(book)
        checkout_user.save()
        return HttpResponseRedirect(reverse('books_page', kwargs={'id': book_id}))