from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic
from .models import Author, Book, Comment, Rating, BookAuthorLink, Publisher, Tag, BookTagLink, BookRatingLink, Data, Identifier, Series
from django.http import HttpResponseRedirect
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

class BookListView(generic.ListView):
    model = Book

    def dispatch(self, *args, **kwargs):
        return super(BookListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # Annotate the books with ratings, tags, etc
        # books = Book.objects.annotate(
        queryset = Book.objects.prefetch_related("tags", "ratings")
        return queryset


class BookDetailView(generic.DetailView):
    model = Book

    def dispatch(self, *args, **kwargs):
        return super(BookDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        try:
            context['comment'] = Comment.objects.get(
                book=context["object"].id).text
        except:
            pass
        context["imgpath"] = context["object"].path + "/cover.jpg"
        download = Data.objects.get(book=context["object"].id)
        context["download"] = f"{context['object'].path}/{download.name}.{download.format.lower()}"
        return context
