from io import RawIOBase
import requests
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from book.templatetags.book_extras import get_readable, get_image
from django.contrib.auth.decorators import login_required
from book.models import Book
from book.forms import BookSearchForm
from notification.models import Notifications
from book.models import Book

# Create your views here.


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('books_page'))
    else:
        template_name = 'index.html'
        book = Book.objects.all()
        context = {"book": book}
        return render(request, template_name, context)


def book_detail(request, id):
    try:
        template_name = 'book/book_detail.html'
        book = Book.objects.get(id=id)
        context = {'book': book}
        return render(request, template_name, context)
    except ObjectDoesNotExist:
        return render(request, 'book/book_error.html')

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

        return redirect(reverse("book_detail_page", args={book.id}))

    except ObjectDoesNotExist:
        response = requests.get(f'http://gutendex.com/books/{id}')
        data = response.json()

        new_book = Book(
            gutenberg_id=data["id"],
            title=data["title"],
            author=data["authors"][0]["name"] if data["authors"] else data["translators"][0]["name"],
            copies_available=1,
            text=get_readable(data["formats"]),
            image_url=get_image(data["formats"])
        )

        new_book.save()

        return redirect(reverse("book_detail_page", args={new_book.id}))


def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'book/all_books.html', {'books': books})


def book_subjects_view(request):
    ...