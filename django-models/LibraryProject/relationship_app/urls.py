from django.urls import path, include
from .views import list_books, LibraryDetailView
from .views import login_view, logout_view, register_view

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('', include('relationship_app.urls')),
        path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
