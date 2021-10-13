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
#   This will redirect to the home page or user detail page, once they are finished
        return HttpResponseRedirect(reverse('book_detail_page', kwargs={'id': id}))
#   This is just placeholder text for now, pending proper error handling
    return HttpResponse('Something went wrong')

