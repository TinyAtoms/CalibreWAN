import logging

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic

from .forms import BookFilterForm, SearchForm
from .http_basic_auth import logged_in_or_basicauth
from .models import Author, Book, Comment, Tag, Data, \
    Series, Language, Publisher, Rating

logger = logging.getLogger(__name__)


@logged_in_or_basicauth("CalibreWAN")
def OPDS_feed_view(request):
    """
    OPDS aquisition feed, borked atm
    :param request:
    :return:
    """
    queryset = Book.objects.prefetch_related("tags", "ratings", "series", "authors", "data_set", "publishers",
                                             "languages", "identifier_set").order_by("id")
    template = loader.get_template('library/opds_aquisition.xml')
    paginator = Paginator(queryset, 100)  # Show 100 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return HttpResponse(template.render(context, request), content_type="text/xml")


class BookDetailView(LoginRequiredMixin, generic.DetailView):
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
        book = context["object"]
        try:
            context['comment'] = Comment.objects.get(book=book.id).text
        except Comment.DoesNotExist:
            pass
        context["imgpath"] =  book.path + "/cover.jpg"
        formats = Data.objects.filter(book=book.id)
        context["downloads"] = []
        for f in formats:
            context["downloads"].append({
                "url" :  f"{book.path}/{f.name}.{f.format.lower()}",
                "format" : f.format.lower(),
                "id" : f.id,
                "reverser" : f
            })
        return context


class DataDetailView(LoginRequiredMixin, generic.DetailView):
    """
    A book detail view, intended to display js readers for specific formats
    """
    model = Data

    def dispatch(self, *args, **kwargs):
        return super(DataDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data and add it to the context
        book = context["object"].book
        data = context["object"]
        context["format"] = data.format.lower()
        context["url"] =  f"{book.path}/{data.name}.{data.format.lower()}"
        context["id"] = data.id
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
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Language.objects.none()
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(lang_code__istartswith=self.q).order_by("lang_code")
        return qs


class SeriesComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """
    Autocomplete for series
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

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
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

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

    def filter_books_get(self, filterset):
        """
        does the actual filtering for get requests
        :param filterset: dictionary with filters
        :return: queryset
        """
        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
        for i in filterset.items():
            if not i[1]:
                continue
            books = books.filter(i)
        return books.distinct()

    def filter_books_post(self, filterset):
        """
        does the actual filtering for post requests
        :param filterset: dictionary with filters
        :return: queryset
        """
        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
        # filter multiSelect fields
        multiple = {"authors": None, "series": None, "tags": None}
        for k, v in multiple.items():
            is_and = filterset.pop(f"{k}_andor")
            items = filterset.pop(k)
            if not items:  # empty MultiSelect field
                continue
            if is_and:  # and filtering
                for i in items:
                    books = books.filter((f"{k}__id", i.id))
            else:  # or filtering
                books = books.filter((f"{k}__in", items))

        # filter normal fields
        for i in filterset.items():
            if not i[1]:
                continue
            books = books.filter(i)
        return books


class SearchResultsView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'library/book_list.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, *args, **kwargs):
        return super(SearchResultsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):  # new
        form = SearchForm(data=self.request.GET)
        if not form.is_valid():
            return Book.objects.none()
        generic_query = form.cleaned_data.get("generic")
        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
        if generic_query:
            author_obj = Author.objects.filter(name__icontains=generic_query).first()
            if not author_obj:
                author_id = -1
            else:
                author_id = author_obj.id
            identifier = generic_query.replace("-", "")
            books = books.filter(
                Q(sort__icontains=generic_query) |
                Q(author_sort__icontains=generic_query) |
                Q(authors__id=author_id) |
                Q(identifier__val=identifier)
            ).distinct()
        return books



## list views, to be moved over to a resultview
class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    ordering = ['sort']

    def dispatch(self, *args, **kwargs):
        return super(AuthorListView, self).dispatch(*args, **kwargs)





class PublisherListView(LoginRequiredMixin, generic.ListView):
    model = Publisher
    ordering = ['name']

    def dispatch(self, *args, **kwargs):
        return super(PublisherListView, self).dispatch(*args, **kwargs)


class RatingListView(LoginRequiredMixin, generic.ListView):
    model = Rating
    ordering = ['rating']

    def dispatch(self, *args, **kwargs):
        return super(RatingListView, self).dispatch(*args, **kwargs)


class SeriesListView(LoginRequiredMixin, generic.ListView):  # make url entry and template, sometime
    model = Series
    ordering = ['name']

    def dispatch(self, *args, **kwargs):
        return super(SeriesListView, self).dispatch(*args, **kwargs)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    ordering = ['name']

    def dispatch(self, *args, **kwargs):
        return super(TagListView, self).dispatch(*args, **kwargs)