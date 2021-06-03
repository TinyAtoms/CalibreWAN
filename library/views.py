import logging

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from .forms import BookFilterForm, SearchForm
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
    """
    A book detail view, intended to display info about a specific book
    """
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
    """
    Autocomplete api thing for titles.
    """

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Book.objects.none()
        qs = Book.objects.all()
        if self.q:
            qs = qs.filter(title__icontains=self.q).order_by("title")
        return qs


class AuthorComplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete thing for authors, for the FilterView
    """

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Author.objects.none()
        qs = Author.objects.all().order_by("sort")
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class TagComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """
    Autocomplete thing for tags, for the FilterView
    """
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
    """
    Autocomplete thing for languages, for the FilterView
    """

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Language.objects.none()
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(lang_code__istartswith=self.q).order_by("lang_code")
        return qs


class SeriesComplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete for series
    """
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
    """
    Advanced book filtering. Can filter by
    1. authors (and/or)
    2. tags (and/or)
    3. Series (and/or)
    4. languages
    5. ratings (greater or equal to )
    6. pubdate ranges
    7. added to calibre ranges
    """
    def get(self, request, *args, **kwargs):
        """
        Hijacked this to substitute for various X_detail pages, filters book where
        for example, book__authors__id=1
        :param request:
        :param args:
        :param kwargs: things to filter for
        :return: rendered template
        """
        context = {'form': BookFilterForm(), "book_list": self.filter_books_get(kwargs)}
        return render(request, 'library/results.html', context)

    def post(self, request, *args, **kwargs):
        """
        Used for the filtering process.
        Gets clean data from the form and filters it.
        :param request:
        :param kwargs:
        :return: rendered template
        """
        form = BookFilterForm(data=request.POST)
        context = {'form': form}
        if not form.is_valid():
            return render(request, 'library/results.html', context)
        filter_dict = form.cleaned_data
        context["book_list"] = self.filter_books_post(filter_dict)
        return render(request, 'library/results.html', context)

    def filter_books_get(self, filter):
        """
        does the actual filtering for get requests
        :param filter: dictionary with filters
        :return: queryset
        """
        books = Book.objects.all()
        for i in filter.items():
            if not i[1]:
                continue
            books = books.filter(i)
        return books.distinct()

    def filter_books_post(self, filter):
        """
        does the actual filtering for post requests
        :param filter: dictionary with filters
        :return: queryset
        """
        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
        # filter multiSelect fields
        multiple = {"authors": None, "series": None, "tags": None}
        for k, v in multiple.items():
            is_and = filter.pop(f"{k}_andor")
            items = filter.pop(k)
            if not items:  # empty MultiSelect field
                continue
            if is_and:  # and filtering
                for i in items:
                    books = books.filter((f"{k}__id", i.id))
            else:  # or filtering
                books = books.filter((f"{k}__in", items))

        # filter normal fields
        for i in filter.items():
            if not i[1]:
                continue
            books = books.filter(i)
        return books


class SearchResultsView(generic.ListView):  # no clue if this is secure.
    # according to this https://stackoverflow.com/questions/13574043/how-do-django-forms-sanitize-text-input-to-prevent-sql-injection-xss-etc
    # it is
    model = Book
    template_name = 'book_list.html'

    def dispatch(self, *args, **kwargs):
        return super(SearchResultsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):  # new
        form = SearchForm(data=self.request.GET)
        if not form.is_valid():
            return Book.objects.none()
        generic = form.cleaned_data.get("generic")
        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
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
