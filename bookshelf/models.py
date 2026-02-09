from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['-created_at']


class Shelf(models.Model):
    SHELF_CHOICES = [
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('read', 'Read'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelves')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='shelved_by')
    shelf_type = models.CharField(max_length=20, choices=SHELF_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_shelf_type_display()})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"
