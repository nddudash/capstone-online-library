"""config URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from book.views import book_add_search_view, book_add_commit_view, book_detail, book_list_view, index_view
from custom_user.views import LoginView, LogoutView, SignUpView, user_profile_view, edit_user_view, CustomUserDeleteView
from reservations.views import reservation_view, remove_reservation_view
from checkout.views import checkout_book_view, return_book_view
from notification.views import notifications_view, no_nots_view
urlpatterns = [
    path('', index_view, name="homepage"),
    path('books/add/<int:id>', book_add_commit_view, name='AddBookView'),
    path('books/add/', book_add_search_view, name='AddBookView'),
    path('admin/', admin.site.urls),
    path('reserve/<int:id>/', reservation_view, name='reserve'),
    path('remove_reservation/<int:id>/', remove_reservation_view, name='remove_reservation'),
    path('book_detail/<int:id>/', book_detail, name='book_detail_page'),
    path('notifications/<int:user_id>/', notifications_view, name='notification'),
    path('nonots/', no_nots_view, name='no_nots'),
    # Make sure the login URL is consistent with the LOGIN_URL in settings.py!
    path('login_view/', LoginView.as_view(), name='login'),
    path('logout_view/', LogoutView.as_view(), name='logout'),
    path('sign_up_view/', SignUpView.as_view(), name='sign_up'),
    path('all_books/', book_list_view, name='books_page'),
    path('checkout/<int:book_id>/', checkout_book_view, name='checkout'),
    path('return/<int:book_id>/', return_book_view, name='return'),
    path('edit/<int:edit_id>/', edit_user_view, name='edit'),
    path('profile/<int:id>/', user_profile_view, name='profile_page'),
    path('delete_user/<int:pk>/', CustomUserDeleteView.as_view(), name='delete_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
