from django import forms
from book.models import Book

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields =  ['title']
        
class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)
    author = forms.CharField(max_length=255, required=False)