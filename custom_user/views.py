from django import template
from django.db import IntegrityError
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from book.models import Book
from custom_user.forms import UserForm
from custom_user.models import CustomUser

from django.contrib.auth import login, authenticate,  logout


# Create your views here.
def user_profile_view(request, id):
    profiles = CustomUser.objects.get(id=id)
    books = Book.objects.all()
    return render(request, 'profile.html', {'profiles': profiles, 'books': books})

# def login_view(request):
#     if request.method == "POST":
#         forms = UserForm(request.POST)
#         if forms.is_valid():
#             data = forms.cleaned_data
#             user = authenticate(
#                 request, username=data['username'], password=data['password'])
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect(request.GET.get('next', reverse('book_list')))
#     forms = UserForm()
#     return render(request, 'generic.html', {"forms": forms})


class LoginView(BaseLoginView):
    template_name = "generic.html"
    form = UserForm
    # TODO: Redirect to Home Page!
    next_page = reverse_lazy('books_page')
    extra_context = {'header': 'Login'}


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(request.GET.get('next', reverse('book_list')))

class LogoutView(BaseLogoutView):
    # TODO: Redirect to Home Page!
    next_page = reverse_lazy('books_page')


# def sign_up_view(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_user = CustomUser.objects.create(
#                 username=data['username'],
#                 password=data['password']
#             )
#             if new_user:
#                 login(request, new_user)
#                 return HttpResponseRedirect(
#                     request.GET.get("next", reverse('books_page'))
#                 )
#             return HttpResponseRedirect(reverse('books_page'))
#     else:

#         form = UserForm()
#     return render(request, 'generic.html', {"form": form})

class SignUpView(FormView):
    template_name = "generic.html"
    form_class = UserForm
    extra_context = {"header": "Signup"}

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            new_user = CustomUser.objects.create(
                username=data['username'],
                password=data['password']
            )

            if new_user:
                login(self.request, new_user)
                # TODO: Redirect to Home!
                return redirect(reverse('books_page'))

        except IntegrityError:
            form.add_error(
                "username", "That Username is unavailable! Please choose another."
            )
            return render(self.request, self.template_name, {"form": form, 'header': 'Signup'})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form, 'header': 'Signup'})
