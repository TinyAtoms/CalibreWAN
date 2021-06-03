import logging

from django.urls import path

from . import views

logger = logging.getLogger(__name__)

urlpatterns = [
    # Autocomplete "api" for filter form
    path("author-autocomplete/", views.AuthorComplete.as_view(), name="author-autocomplete"),
    path("tag-autocomplete/", views.TagComplete.as_view(), name="tag-autocomplete"),
    path("lang-autocomplete/", views.LanguageComplete.as_view(), name="lang-autocomplete"),
    path("series-autocomplete/", views.SeriesComplete.as_view(), name="series-autocomplete"),
    path("title-autocomplete/", views.TitleComplete.as_view(), name="title-autocomplete"),


    path('results/', views.SearchResultsView.as_view(), name='results'),
    path("filter/", views.FilterView.as_view(), name="filter"),
    path('books/', views.FilterView.as_view(), name='books'),
    path("tag/<int:tags__id>", views.FilterView.as_view(), name="tag-detail-view"),
    path("author/<int:authors__id>", views.FilterView.as_view(), name="author-detail-view"),
    path("series/<int:series__id>", views.FilterView.as_view(), name="series-detail-view"),
    path("publisher/<int:publishers>", views.FilterView.as_view(), name="publisher-detail-view"),
    path("rating/<int:ratings__rating>", views.FilterView.as_view(), name="publisher-detail-view"),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail-view'),

]
