from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils.decorators import method_decorator
from book.models import Book
from custom_user.forms import UserForm
from custom_user.models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate,  logout
from django.views.generic.edit import DeleteView


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
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('books_page')))
    forms = UserForm()
    return render(request, 'generic.html', {"forms": forms})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', reverse('books_page')))


def sign_up_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = CustomUser.objects.create(
                username=data['username'],
                password=data['password']
            )
            if new_user:
                login(request, new_user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse('books_page'))
                )
            return HttpResponseRedirect(reverse('books_page'))
    else:

        forms = UserForm()
    return render(request, 'generic.html', {"forms": forms})

class CustomUserDeleteView(DeleteView):
    model = CustomUser
    template_name = "customuser_confirm_delete.html"
    def get_success_url(self):
        return reverse('login_view')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomUserDeleteView, self).dispatch(request, *args, **kwargs)
