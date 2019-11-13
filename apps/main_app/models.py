from django.db import models
from datetime import date, datetime
import re

# Create your models here.


class UserManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['full_name']) < 2:
            errors['full_name'] = "The full name field is required and should be at least 2 characters long."
        if len(post_data['alias']) < 2:
            errors['alias'] = "The alias field is required and should be at least 2 characters long."
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = ("Invalid email address or email!")
        if User.objects.filter(email=post_data['email']).exists():
            errors['email'] = ("Email already exists, try logging in.")
        if len(post_data['password']) < 8 or len(post_data['password']) == 0:
            errors['password'] = "The password field is required and should be at least 8 characters long."
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Your passwords do not match, try again!"
        return errors


class User(models.Model):
    full_name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # books_uploaded
    # reviews

    def __repr__(self):
        return f"<User Object: {self.id} {self.full_name} {self.alias}>"


class BookManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['title']) == 0:
            errors['title'] = "The title of the book is required, please enter it!"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=60)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    author = models.ForeignKey('Author', related_name="books_for_this_author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    # reviews_for_book

    def __repr__(self):
        return f"<Book Object: {self.id} {self.title} {self.desc}>"


class ReviewManager(models.Manager):
    def validator(self, post_data):
        errors = {}
        if len(post_data['content']) == 0:
            errors['content'] = "The review of this book is required, please enter it!"
        return errors


class Review(models.Model):
    content = models.TextField()
    star = models.PositiveIntegerField()
    book = models.ForeignKey(Book, related_name="reviews_for_book")
    creater = models.ForeignKey(User, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # review for book
    objects = ReviewManager()

    def __repr__(self):
        return f"<Review Object: {self.id} {self.content} {self.star}>"


class Author(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # books_for_this_author

    def __repr__(self):
        return f"<Author Object: {self.id} {self.name}>"
