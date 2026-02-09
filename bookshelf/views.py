from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Book, Shelf, Review
from .forms import ReviewForm, BookForm


def home(request):
    recent_books = Book.objects.all()[:12]
    view_mode = request.GET.get('view', 'grid')  # grid or list
    return render(request, 'bookshelf/home.html', {
        'recent_books': recent_books,
        'view_mode': view_mode
    })


def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    view_mode = request.GET.get('view', 'grid')  # grid or list
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(books, 12)  # 12 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookshelf/book_list.html', {
        'page_obj': page_obj,
        'query': query,
        'view_mode': view_mode,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.select_related('user').all()
    user_shelf = None
    user_review = None
    
    if request.user.is_authenticated:
        user_shelf = Shelf.objects.filter(user=request.user, book=book).first()
        user_review = Review.objects.filter(user=request.user, book=book).first()
    
    return render(request, 'bookshelf/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'user_shelf': user_shelf,
        'user_review': user_review,
    })


@login_required
def add_to_shelf(request, pk):
    book = get_object_or_404(Book, pk=pk)
    shelf_type = request.POST.get('shelf_type', 'want_to_read')
    
    shelf, created = Shelf.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={'shelf_type': shelf_type}
    )
    
    if created:
        messages.success(request, f'Added "{book.title}" to {shelf.get_shelf_type_display()}')
    else:
        messages.success(request, f'Moved "{book.title}" to {shelf.get_shelf_type_display()}')
    
    return redirect('book_detail', pk=pk)


@login_required
def remove_from_shelf(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Shelf.objects.filter(user=request.user, book=book).delete()
    messages.success(request, f'Removed "{book.title}" from your shelves')
    return redirect('book_detail', pk=pk)


@login_required
def update_date_finished(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        shelf = Shelf.objects.filter(user=request.user, book=book, shelf_type='read').first()
        if shelf:
            date_str = request.POST.get('date_finished')
            if date_str:
                from datetime import datetime
                shelf.date_finished = datetime.strptime(date_str, '%Y-%m-%d').date()
                shelf.save()
                messages.success(request, 'Date finished updated!')
            else:
                shelf.date_finished = None
                shelf.save()
                messages.success(request, 'Date finished cleared!')
    return redirect('book_detail', pk=pk)


@login_required
def my_shelves(request):
    shelf_type = request.GET.get('shelf', 'all')
    view_mode = request.GET.get('view', 'grid')  # grid or list
    
    if shelf_type == 'all':
        shelved_books = Shelf.objects.filter(user=request.user).select_related('book')
    else:
        shelved_books = Shelf.objects.filter(
            user=request.user,
            shelf_type=shelf_type
        ).select_related('book')
    
    # Get counts for each shelf
    shelf_counts = {
        'all': Shelf.objects.filter(user=request.user).count(),
        'want_to_read': Shelf.objects.filter(user=request.user, shelf_type='want_to_read').count(),
        'currently_reading': Shelf.objects.filter(user=request.user, shelf_type='currently_reading').count(),
        'read': Shelf.objects.filter(user=request.user, shelf_type='read').count(),
    }
    
    # Pagination
    paginator = Paginator(shelved_books, 12)  # 12 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookshelf/my_shelves.html', {
        'page_obj': page_obj,
        'current_shelf': shelf_type,
        'view_mode': view_mode,
        'shelf_counts': shelf_counts,
    })


@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'content': form.cleaned_data['content']}
            )
            messages.success(request, 'Review saved!')
            return redirect('book_detail', pk=pk)
    else:
        existing_review = Review.objects.filter(user=request.user, book=book).first()
        form = ReviewForm(instance=existing_review)
    
    return render(request, 'bookshelf/add_review.html', {
        'form': form,
        'book': book,
    })


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    book_pk = review.book.pk
    review.delete()
    messages.success(request, 'Review deleted')
    return redirect('book_detail', pk=book_pk)


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Added "{book.title}"!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/add_book.html', {'form': form})


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Updated "{book.title}"!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Deleted "{title}"')
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})
