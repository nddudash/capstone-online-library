from django.shortcuts import render, HttpResponse, HttpResponseRedirect
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
        print(checkout_user.checked_out_books.all())
#   This will redirect to the home page or user detail page, once they are finished
        return HttpResponse('You have successfully checked out this book')
#   This is just placeholder text for now, pending proper error handling
    return HttpResponse('Something went wrong')

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
        print(checkout_user.checked_out_books.all())
#   This will redirect to the home page or user detail page, once they are finished
        return HttpResponse('You have successfully returned this book')
#   This is just placeholder text for now, pending proper error handling
    return HttpResponse('Something went wrong')