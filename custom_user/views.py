from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.hashers import make_password
from book.models import Book
from custom_user.forms import UserForm
from custom_user.models import CustomUser
from django.contrib.auth import login, authenticate,  logout, update_session_auth_hash
from django.views.generic.edit import DeleteView


# Create your views here.
def user_profile_view(request, id):
    try:
        profiles = CustomUser.objects.get(id=id)
        books = Book.objects.all()
        return render(request, 'profile.html', {'profiles': profiles, 'books': books})
    except ObjectDoesNotExist:
        return render(request, 'user_error.html')


class LoginView(BaseLoginView):
    template_name = "generic.html"
    form = UserForm
    next_page = reverse_lazy('books_page')
    extra_context = {'header': 'Login'}


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('homepage')


class SignUpView(FormView):
    template_name = "generic.html"
    form_class = UserForm
    extra_context = {"header": "Signup"}

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            new_user = CustomUser.objects.create(
                username=data['username'],
                password=make_password(data['password'])
            )

            if new_user:
                login(self.request, new_user)
                return redirect(reverse('books_page'))

        except IntegrityError:
            form.add_error(
                "username", "That Username is unavailable! Please choose another."
            )
            return render(self.request, self.template_name, {"form": form, 'header': 'Signup'})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form, 'header': 'Signup'})


@login_required
def edit_user_view(request, edit_id):
    form = UserForm
    user = CustomUser.objects.get(id=edit_id)
    if request.method == 'POST':
        info = UserForm(request.POST)
        if info.is_valid():
            data = info.cleaned_data
            user.username = data['username']
            user.password = make_password(data['password'])
            user.save()
            print("Success", user.password)
            # CITATION - https://stackoverflow.com/questions/30821795/django-user-logged-out-after-password-change
            update_session_auth_hash(request, user)
            return redirect(reverse('books_page'))

    form = UserForm(
        initial={'username': user.username, 'password': user.password})

    return render(request, 'generic.html', {'form': form, 'header': 'Edit Account'})

# CITATION https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview


class CustomUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.get_object().username == self.request.user.username
    model = CustomUser
    template_name = 'customuser_confirm_delete.html'
    login_url = 'login_view'

    def get_success_url(self):
        return (reverse('login'))


# Keeping the non-generic views as comments just in case
#
#
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
#
#
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(request.GET.get('next', reverse('book_list')))
#
#
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
