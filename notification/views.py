from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom_user.models import CustomUser
from notification.models import Notifications


# Create your views here.
@login_required
def notifications_view(request, user_id):
    context = {
        "logged_in": request.user.is_authenticated,
        "user": request.user,
        "notifications_user": CustomUser.objects.get(id__exact=user_id)
    }

    notifications = Notifications.objects.filter(
        notified_user=request.user)
    notifications_copy = list(notifications)
    context["notifications"] = notifications_copy
    # CITATION - https://stackoverflow.com/questions/9143262/delete-multiple-objects-in-django
    notifications.delete()
    
    return render(request, "notifications.html", context)
