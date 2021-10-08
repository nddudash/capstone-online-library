from django.contrib.auth.models import User
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from book.models import Book, Comment
from book.forms import BookSearchForm, CommentForm
from custom_user.forms import UserForm
from book.templatetags.book_extras import get_readable, get_image
from django.contrib.auth.decorators import login_required
from notification.models import Notifications
from custom_user.models import CustomUser

# Create your views here.


def index_view(request):
    template_name = 'index.html'
    book = Book.objects.all()
    context = {"book": book}
    return render(request, template_name, context)


def book_detail(request, id):
    template_name = 'book/book_detail.html'
    book = Book.objects.get(id=id)
    context = {'book': book}
    return render(request, template_name, context)


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


def book_add_commit_view(request, id):

    try:
        book = Book.objects.get(gutenberg_id__exact=id)

        book.copies_available += 1

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
            image_url=get_image(data["formats"])
        )

        new_book.save()

        # TODO: Redirect to Book Detail View
        return HttpResponse("You've added a book")


def BookList_view(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books': books})


def edit_user_view(request, edit_id):
    form = CustomUser.objects.get(id=edit_id)
    if request.method == 'POST':
        info = UserForm(request.POST)
        if info.is_valid():
            data = info.cleaned_data
            form.username = data['username']
            form.password = data['password']
            form.save()
            return HttpResponseRedirect('home')
    forms = UserForm(
        initial={'username': form.username, 'password': form.password})
    return render(request, 'generic.html', {'forms': forms})


def comment_view(request, pk):
    post = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        comments = CommentForm(request.POST)
        if comments.is_valid():
            comment = comments.save(active=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect('home')
        else:
            form = CommentForm()
            return render(request, 'generic.html', {'form': form, 'comments': comments})
    # return render(request, 'book/all_books.html', {'books': books})
    # redirect here
