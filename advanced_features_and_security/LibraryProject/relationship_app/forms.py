from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from bookshelf.models import CustomUser

class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth", "profile_photo")