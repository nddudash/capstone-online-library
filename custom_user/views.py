from django.db import models
from django.shortcuts import render, HttpResponseRedirect, reverse
from book.models import Book
from custom_user.forms import UserForm
from custom_user.models import CustomUser

from django.contrib.auth import login, authenticate,  logout


# Create your views here.
def user_profile_view(request,id):
  profiles = CustomUser.objects.get(id=id)
  books = Book.objects.all()
  return render(request, 'profile.html', {'profiles': profiles, 'books': books})

def login_view(request):
    if request.method == "POST":
        forms = UserForm(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('book_list')))
    forms = UserForm()
    return render(request, 'generic.html', {"forms": forms})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', reverse('book_list')))


def sign_up_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = CustomUser.objects.create(
                username = data['username'],
                password = data['password']
            )
            if new_user:
                login(request, new_user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("book_list"))
                )
            return HttpResponseRedirect(reverse("book_list"))
    else:
        
        forms = UserForm()
    return render(request, 'generic.html', {"forms": forms})
