from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'main_app/index.html')


def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(
            full_name=request.POST['full_name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash)
        if user:
            request.session['uid'] = user.id
        else:
            return redirect('/')
    return redirect('/books')


def login(request):
    user_list = User.objects.filter(email=request.POST['email'])
    if len(user_list) > 0:
        logged_user = user_list[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/books')
    messages.error(request, "Invalid email and/or password")
    return redirect('/')


# Books Home Page
def books(request):
    if 'uid' not in request.session:
        messages.error(
            request, "You have not logged in or registered, please log in or register.")
        return redirect('/')
    latest_three_reviews = Review.objects.all().order_by('-created_at')[:3]

    context = {
        'user': User.objects.get(id=request.session['uid']),
        'all_reviews': Review.objects.all(),
        'latest_three_reviews': latest_three_reviews
    }
    return render(request, 'main_app/books.html', context)

# Add Book and Review


def add_book_view(request):
    context = {
        'all_authors': Author.objects.all()
    }
    return render(request, 'main_app/add_book.html', context)

# Add book html template


def add_book(request):
    book_errors = Book.objects.validator(request.POST)
    review_errors = Review.objects.validator(request.POST)
    if len(book_errors) > 0 or len(review_errors) > 0:
        for key, value in book_errors.items():
            messages.error(request, value)
        for key, value in review_errors.items():
            messages.error(request, value)
        return redirect('/add_book_view')
    else:
        print(request.POST)
        if len(request.POST['new_author']) == 0:
            author = Author.objects.get(name=request.POST['old_author'])
        else:
            author = Author.objects.create(name=request.POST['new_author'])
            uploader = User.objects.get(id=request.session['uid'])
            book = Book.objects.create(
                title=request.POST['title'], uploaded_by=uploader, author=author)
            review = Review.objects.create(content=request.POST['content'], star=int(
                request.POST['star']), book=book, creater=uploader)
        print(review)
    return redirect(f'/books/{book.id}')

# Book profile html template


def book_profile(request, book_id):
    book = Book.objects.get(id=book_id)

    context = {
        'book': book,
        'logged_in_user': User.objects.get(id=request.session['uid']),
        'book_reviews': book.reviews_for_book.all()
    }
    return render(request, 'main_app/book_profile.html', context)

# Add Review


def add_review(request, book_id):
    review_errors = Review.objects.validator(request.POST)
    if len(review_errors) > 0:
        for key, value in review_errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    else:
        uploader = User.objects.get(id=request.session['uid'])
        book = Book.objects.get(id=book_id)
        Review.objects.create(content=request.POST['content'], star=int(
            request.POST['star']), book=book, creater=uploader)
    return redirect(f'/books/{book_id}')

# User Profile View


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user,
        'user_reviews': Review.objects.filter(creater=user),
        'user_reviews_count': Review.objects.filter(creater=user).count()
    }
    return render(request, 'main_app/user_profile.html', context)

# Delete review


def delete_review(request, review_id, user_id):
    review_to_delete = Review.objects.get(id=review_id)
    review_to_delete.delete()
    return redirect(f'/users/{user_id}')

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out.")
    return redirect('/')
