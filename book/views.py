import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from book.templatetags.book_extras import get_readable
from django.contrib.auth.decorators import login_required
from book.models import Book
from book.forms import BookSearchForm
from notification.models import Notifications
from book.models import Book
from custom_user.models import CustomUser

# Create your views here.
<<<<<<< HEAD
=======


>>>>>>> devIbe-merge
def index_view(request):
    template_name = 'index.html'
    book = Book.objects.all()
    context = {"book": book}
    return render(request, template_name, context)


<<<<<<< HEAD
def book_detail(request,id):
  template_name = 'book_detail.html'
  book = Book.objects.get(id=id)
  context = {'book': book}
  return render(request, template_name, context)
=======
def book_detail(request, id):
    template_name = 'book/book_detail.html'
    book = Book.objects.get(id=id)
    user = CustomUser.objects.get(id=request.user.id)
    context = {'book': book, 'user': user}
    return render(request, template_name, context)
>>>>>>> devIbe-merge


def book_add_search_view(request):
    context = {
        "form": BookSearchForm,
        "results": {}
    }

    if request.method == "POST":
        form = BookSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            search_str = 'http://gutendex.com/books?search='

            if data["title"]:
                if len(search_str) > 33:
                    search_str += "%20"
                cleaned_title = data["title"].replace(" ", "%20")
                search_str += cleaned_title
            if data["author"]:
                if len(search_str) > 33:
                    search_str += "%20"
                cleaned_author = data["author"].replace(" ", "%20")
                search_str += cleaned_author

            response = requests.get(search_str)
            data = response.json()
            context["results"] = data["results"]

    return render(request, 'book/book_search_and_add.html', context)


@login_required
def book_add_commit_view(request, id):

    try:
        book = Book.objects.get(gutenberg_id__exact=id)

        book.copies_available += 1
        if book.is_reserved:
            notification = Notifications.objects.create(
                user=book.customuser_set.first(),
                book=book,
                exclamation=True,
            )
            notification.save()
        book.save()

        # TODO: Redirect to Book Detail View
        return HttpResponse("You've added a book")

    except ObjectDoesNotExist:
        response = requests.get(f'http://gutendex.com/books/{id}')
        data = response.json()

        new_book = Book(
            gutenberg_id=data["id"],
            title=data["title"],
            author=data["authors"][0]["name"],
            copies_available=1,
            text=get_readable(data["formats"]),
        )

        new_book.save()

        # TODO: Redirect to Book Detail View
        return HttpResponse("You've added a book")


def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'book/all_books.html', {'books': books})
