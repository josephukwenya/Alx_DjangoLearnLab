from rest_framework import serializers
from .models import Book, Author
from django.utils import timezone

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
        current_year = timezone.now().year
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