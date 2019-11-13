from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    # List of books
    url(r'^books$', views.books),
    # Add book html template
    url(r'^add_book_view$', views.add_book_view),
    # Add book and review
    url(r'^add_book$', views.add_book),
    # Book profile html template
    url(r'^books/(?P<book_id>\d+)$', views.book_profile),
    # Add review
    url(r'^books/add_review/(?P<book_id>\d+)$', views.add_review),
    # User Profile View
    url(r'^users/(?P<user_id>\d+)$', views.user_profile),
    # Delete review
    url(r'^users/delete_review/(?P<review_id>\d+)/(?P<user_id>\d+)$', views.delete_review),
    url(r'^logout$', views.logout),
]
