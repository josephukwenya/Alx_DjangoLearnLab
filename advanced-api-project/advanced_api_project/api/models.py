from django.db import models

# Create your models here.
class Author(models.Model):
    # Author with a name
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
  # Book with title, year, and author relationship
  title = models.CharField(max_length=200)
  publication_year = models.IntegerField()
  author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.title} ({self.publication_year})"