Got it ✅ — here’s the complete step-by-step implementation for your **"Setting Up a New Django Project with Custom Serializers"** task, following the exact requirements.

---

## **Step 1 — Install Django & DRF**

In your terminal:

```bash
# Create project directory
mkdir advanced-api-project && cd advanced-api-project

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install Django & DRF
pip install django djangorestframework

# Create Django project (avoids nested folder)
django-admin startproject advanced_api_project .

# Create the 'api' app
python manage.py startapp api
```

---

## **Step 2 — Configure `settings.py`**

Open **`advanced_api_project/settings.py`** and update:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',

    # Local apps
    'api',
]

# (Optional) DRF default settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

💡 We’re keeping the **SQLite** database (default) for simplicity.

---

## **Step 3 — Define Models in `api/models.py`**

```python
from django.db import models

class Author(models.Model):
    """
    Author model:
    Stores information about book authors.
    One author can have multiple books (One-to-Many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    Stores details about books.
    Each book is linked to a specific author.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # Allows reverse access: author.books.all()
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **Step 4 — Create Custom Serializers in `api/serializers.py`**

```python
from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer:
    Serializes all fields of the Book model.
    Includes validation to ensure the publication year is not in the future.
    """

    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """Ensure publication year is not in the future."""
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. ({current_year})"
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer:
    Serializes author details along with all related books (nested serialization).
    """
    books = BookSerializer(many=True, read_only=True)
    # 'books' comes from the related_name in Book model

    class Meta:
        model = Author
        fields = ['name', 'books']
```

---

## **Step 5 — Admin Registration in `api/admin.py`**

For easy testing:

```python
from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publication_year', 'author')
```

---

## **Step 6 — Testing in Django Shell**

Run:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Then in **Django shell**:

```bash
python manage.py shell
```

```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create an author
author = Author.objects.create(name="Chinua Achebe")

# Create books
Book.objects.create(title="Things Fall Apart", publication_year=1958, author=author)
Book.objects.create(title="No Longer at Ease", publication_year=1960, author=author)

# Serialize author with nested books
serializer = AuthorSerializer(author)
print(serializer.data)
```

Expected output:

```python
{
    'name': 'Chinua Achebe',
    'books': [
        {'id': 1, 'title': 'Things Fall Apart', 'publication_year': 1958, 'author': 1},
        {'id': 2, 'title': 'No Longer at Ease', 'publication_year': 1960, 'author': 1}
    ]
}
```

---

## **Step 7 — GitHub Repo Setup**

```bash
git init
git add .
git commit -m "Initial commit - Django project with custom serializers"
git branch -M main
git remote add origin https://github.com/<your-username>/Alx_DjangoLearnLab.git
git push -u origin main
```

---

✅ This setup meets all **mandatory requirements**:

- **Custom serializers**
- **Nested relationships** (`Author → Books`)
- **Custom validation** (no future publication years)
- **Documented models & serializers**

---

If you want, I can now **add DRF views and URLs** so that you can test this via Postman instead of only the shell. That way, you’ll have a full API endpoint ready.
