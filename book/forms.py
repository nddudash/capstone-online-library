from django import forms

from book.models import Comment


class BookSearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)
    author = forms.CharField(max_length=255, required=False)


class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ('post')
