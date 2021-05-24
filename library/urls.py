from django.urls import path
from . import views
import logging

logger = logging.getLogger(__name__)

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail-view'),
]
