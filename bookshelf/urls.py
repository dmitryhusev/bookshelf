from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:pk>/add-to-shelf/', views.add_to_shelf, name='add_to_shelf'),
    path('books/<int:pk>/remove-from-shelf/', views.remove_from_shelf, name='remove_from_shelf'),
    path('books/<int:pk>/update-date-finished/', views.update_date_finished, name='update_date_finished'),
    path('books/<int:pk>/review/', views.add_review, name='add_review'),
    path('books/add/', views.add_book, name='add_book'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('my-shelves/', views.my_shelves, name='my_shelves'),
]
