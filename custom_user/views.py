from django.shortcuts import render, HttpResponseRedirect, reverse
from custom_user.forms import UserForm

from django.contrib.auth import login, authenticate,  logout


# Create your views here.


def login(request):
    if request.method == "POST":
        forms = UserForm(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('/')))
    forms = UserForm()
    return render(request, 'generic.html', {"forms": forms})


def logout_view(request):
    logout(request)


def sign_up_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("home"))
                )
            return HttpResponseRedirect(reverse("home"))
    else:
        
        forms = UserForm()
    return render(request, 'generic.html', {"forms": forms})
