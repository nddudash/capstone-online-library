from django.db.models.base import Model
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from book.templatetags.book_extras import get_readable
from book.models import Book
from book.forms import BookSearchForm

# Create your views here.


def book_add_search_view(request):
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


def book_add_commit_view(request, id):
    
    try:
        book = Book.objects.get(gutenberg_id__exact = id)
        print(book)

        book.copies_available += 1

        book.save()

        return HttpResponse("You've added a book")
    
    except ObjectDoesNotExist:
        response = requests.get(f'http://gutendex.com/books/{id}')
        data = response.json()
        
        
        
        new_book = Book(
            gutenberg_id = data["id"],
            title = data["title"],
            author = data["authors"][0]["name"],
            copies_available = 1,
            text=get_readable(data["formats"]),
        )
    
        new_book.save()
        
        return HttpResponse("You've added a book")
    

    
