import logging
from datetime import date

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from .forms import BookFilterForm
from .models import Author, Book, Comment, Tag, Data, \
    Series, Language

logger = logging.getLogger(__name__)


# class BookListView(generic.ListView):
#     model = Book
#
#     def dispatch(self, *args, **kwargs):
#         return super(BookListView, self).dispatch(*args, **kwargs)
#
#     def get_queryset(self):
#         # Annotate the books with ratings, tags, etc
#         # books = Book.objects.annotate(
#         queryset = Book.objects.prefetch_related("tags", "ratings")
#         return queryset


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


class TitleComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Book.objects.none()
        qs = Book.objects.all()
        if self.q:
            qs = qs.filter(title__icontains=self.q).order_by("title")
        return qs


class AuthorComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Author.objects.none()
        qs = Author.objects.all().order_by("sort")
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class TagComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        qs = Tag.objects.all().order_by("name")

        author = self.forwarded.get('authors', None)
        books = Book.objects.all()

        if author:
            author_objs = Author.objects.filter(id__in=author)
            books = books.filter(authors__in=author_objs)
            qs = qs.filter(book__in=books).distinct()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class LanguageComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Language.objects.none()
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(lang_code__istartswith=self.q).order_by("lang_code")
        return qs


class SeriesComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Series.objects.none()
        qs = Series.objects.all().order_by("name")
        books = Book.objects.all().prefetch_related("tags", "ratings", "series", "authors")
        author = self.forwarded.get('authors', None)
        tag = self.forwarded.get('tags', None)
        if author:
            author_objs = Author.objects.filter(id__in=author)
            books = books.filter(authors__in=author_objs).distinct()
            qs = qs.filter(book__in=books).distinct()
        if tag:
            tag_obs = Tag.objects.filter(id__in=tag)
            books = books.filter(tags__in=tag_obs).distinct()
            qs = qs.filter(book__in=books).distinct()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class FilterView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        context = {'form': BookFilterForm(), "book_list": self.filter_books(kwargs)}
        return render(request, 'library/results.html', context)

    def post(self, request, *args, **kwargs):
        form = BookFilterForm(data=request.POST)
        context = {'form': form}
        if not form.is_valid():
            return render(request, 'library/results.html', context)
        POST = self.request.POST
        filter_dict = dict(POST)
        filter_dict.pop("csrfmiddlewaretoken")
        multiple = ["authors", "series", "tags"]
        for k,v in filter_dict.items():
            if k in multiple and v[0] != "": # a multiple choice field filled
                filter_dict[k] = [int(i) for i in v]
            elif v[0] == "": # any field, empty
                filter_dict[k] = None
            else: # any other field, filled
                filter_dict[k] = int(v[0])
        if POST["timestamp_begin_month"]:
            filter_dict["timestamp_begin"] = date(
                int(POST["timestamp_begin_year"]),
                int(POST["timestamp_begin_month"]),
                int(POST["timestamp_begin_day"]))
        if POST["timestamp_end_month"]:
            filter_dict["timestamp_end"] = date(
                int(POST["timestamp_end_year"]),
                int(POST["timestamp_end_month"]),
                int(POST["timestamp_end_day"]))
        context["book_list"] = self.filter_books(filter_dict)
        return render(request, 'library/results.html', context)

    def filter_books(self, filter):
        print(filter) # DEBUG
        authors = filter.get("authors", [])
        author = filter.get("author", 0)
        authors_andor = filter.get("authors_andor")
        tags = filter.get("tags", [])
        tag = filter.get("tag", 0)
        tags_andor = filter.get("tags_andor")
        series = filter.get("series", [])
        series_id = filter.get("series_id", 0)
        series_andor = filter.get("series_andor")
        langs = filter.get("langs")
        publisher = filter.get("publisher", 0)
        rating = filter.get("rating", None)
        rating_lte = filter.get("rating_lte", 0)
        pubyear_begin = filter.get("pubyear_begin", 0)
        pubyear_end = filter.get("pubyear_end", 0)
        timestamp_begin = filter.get("timestamp_begin", None)
        timestamp_end = filter.get("timestamp_end", None)

        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
        if author:
            books = books.filter(authors__id=author)
        if authors and authors_andor:
            for i in authors:
                books = books.filter(authors__id=i)
        elif authors:
            author_objs = Author.objects.filter(id__in=authors)
            books = books.filter(authors__in=author_objs)
        if tag:
            books = books.filter(tags__id=tag)
        if tags and tags_andor:
            for i in tags:
                books = books.filter(tags__id=int(i))
        elif tags:
            tag_objs = Tag.objects.filter(id__in=tags)
            books = books.filter(tags__in=tag_objs)
        if series_id:
            books = books.filter(series__id=series_id)
        if series and series_andor:
            for i in series:
                books = books.filter(series__id=int(i))
        elif series:
            books = books.filter(series__in=series)
        if langs:
            books = books.filter(languages=langs).distinct()
        if publisher:
            books = books.filter(publishers=publisher)
        if rating != None:
            books = books.filter(ratings__rating=rating)
        if rating_lte:
            books = books.filter(ratings__rating__gte=rating_lte)
        if pubyear_begin:
            books = books.filter(pubdate__gte=date(pubyear_begin, 1, 1))
        if pubyear_end:
            books = books.filter(pubdate__lte=date(pubyear_end, 12, 31))
        if timestamp_begin:
            books = books.filter(timestamp__gte=timestamp_begin)
        if timestamp_end:
            books = books.filter(timestamp__lte=timestamp_end)
        print(books.query) # DEBUG
        return books


class SearchResultsView(generic.ListView):  # no clue if this is secure.
    # according to this https://stackoverflow.com/questions/13574043/how-do-django-forms-sanitize-text-input-to-prevent-sql-injection-xss-etc
    # it is
    model = Book
    template_name = 'book_list.html'

    def dispatch(self, *args, **kwargs):
        return super(SearchResultsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):  # new
        generic = self.request.GET.get("generic")
        books = Book.objects.prefetch_related("tags", "ratings")
        if generic:
            author_obj = Author.objects.filter(name__icontains=generic).first()
            if not author_obj:
                author_id = -1
            else:
                author_id = author_obj.id
            books = books.filter(
                Q(sort__icontains=generic) |
                Q(author_sort__icontains=generic) |
                Q(authors__id=author_id) |
                Q(identifier__val=generic)
            ).distinct()
        return books
