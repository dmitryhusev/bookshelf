from django.contrib import admin
from .models import Book, Shelf, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_year', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['published_year', 'created_at']


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'shelf_type', 'added_at']
    list_filter = ['shelf_type', 'added_at']
    search_fields = ['user__username', 'book__title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title', 'content']
