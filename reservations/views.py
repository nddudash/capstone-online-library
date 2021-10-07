from django.shortcuts import render
from book.models import Book
from custom_user.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def reservation_view(request, id):
    user = CustomUser.objects.get(username=request.user.username)
    book = Book.objects.get(id=id)

    if book not in user.checked_out_books.all():
        user.reserved_books.add(book)
        user.save()
#   This will redirect to the home page or user detail page, once they are finished
        return HttpResponse('You have successfully reserved this book')
#   This is just placeholder text for now, pending proper error handling
    return HttpResponse('Something went wrong')

