from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from custom_user.models import CustomUser
from book.models import Book

def checkout_book_view(request, book_id):
    checkout_user = CustomUser.objects.get(username=request.user.username)
    book = Book.objects.get(gutenberg_id__exact=book_id)

    if book.copies_available and not book in checkout_user.checked_out_books.all():
        book.copies_available += -1
        book.save()
        checkout_user.checked_out_books.add(book)
#   This will redirect to the home page or user detail page, once they are finished
        return HttpResponse('You have successfully checked out this book')
#   This is just placeholder text for now, pending proper error handling
    return HttpResponse('Something went wrong')

