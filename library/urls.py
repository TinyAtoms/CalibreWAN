import logging

from django.urls import path

from . import views

logger = logging.getLogger(__name__)

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail-view'),

    path("search/", views.SearchView.as_view(), name="search"),
    path("author-autocomplete/", views.AuthorComplete.as_view(), name="author-autocomplete"),
    path("tag-autocomplete/", views.TagComplete.as_view(), name="tag-autocomplete"),
    path("lang-autocomplete/", views.LanguageComplete.as_view(), name="lang-autocomplete"),
    path("series-autocomplete/", views.SeriesComplete.as_view(), name="series-autocomplete"),

]
