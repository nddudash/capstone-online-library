import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import SafeString
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView
from book.models import Book
from book.forms import BookSearchForm

# Create your views here.


def AddBookView(request):
    context = {
        "form": BookSearchForm,
        "results": {}
    }

    if request.method == "POST":
        form = BookSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)

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

# class AddBookView(LoginRequiredMixin, CreateView):
#     model = models.Book
#     fields = ['title', 'text', 'author']
