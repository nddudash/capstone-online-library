from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom_user.models import CustomUser
from notification.models import Notifications
from book.models import Book


# Create your views here.
@login_required
def notifications_view(request, user_id):
    context = {
        "logged_in": request.user.is_authenticated,
        "user": request.user,
        "notifications_user": CustomUser.objects.get(id__exact=user_id),
    }

    notifications = Notifications.objects.filter(
        user=request.user)
    notifications_copy = notifications
    context["notifications"] = list(notifications_copy)
    print(context["notifications"])
    # CITATION - https://stackoverflow.com/questions/9143262/delete-multiple-objects-in-django
    notifications.delete()
    
    return render(request, "notifications.html", context)

@login_required
def no_nots_view(request):
    return render(request, "no_nots.html")
