from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Author model:
    Stores information about book authors.
    One author can have multiple books (One-to-Many relationship).
    """
    name = models.CharField(max_length=100)

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
        return self.title