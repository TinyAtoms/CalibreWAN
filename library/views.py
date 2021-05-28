import logging

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .forms import BookFilterForm
from .models import Author, Book, Comment, Tag, Data, \
    Series, Language

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


class AuthorComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Author.objects.none()
        qs = Author.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class TagComplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        qs = Tag.objects.all()
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
            qs = qs.filter(lang_code__istartswith=self.q)
        return qs


class SeriesComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Series.objects.none()
        qs = Series.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class SearchView(generic.View):
    def get(self, request, *args, **kwargs):
        form = BookFilterForm({
            "authors_andor": 0,
            "tags_andor": 0,
            "series_andor": 0,

        })
        context = {'form': form}
        return render(request, 'library/results.html', context)

    def post(self, request, *args, **kwargs):
        form = BookFilterForm(data=request.POST)
        context = {'form': form}
        print(form.data)
        if not form.is_valid():
            return render(request, 'library/results.html', context)

        POST = self.request.POST
        title = POST.get('title')
        authors = POST.getlist('authors')
        tags = POST.getlist("tags")
        series = POST.getlist("series")
        langs = POST.get("langs")
        authors_andor = int(POST.get("authors_andor"))
        series_andor = int(POST.get("series_andor"))
        tags_andor = int(POST.get("tags_andor"))
        books = Book.objects.prefetch_related("tags", "ratings", "series", "authors")
        if title:
            books = books.filter(sort__icontains=title)
        if authors:
            if authors_andor:
                for i in authors:
                    books = books.filter(authors__id=int(i))
                # books = books.filter(reduce(operator.and_, (Q(authors__id=int(author)) for author in authors)))
            else:
                author_objs = Author.objects.filter(id__in=authors)
                books = books.filter(authors__in=author_objs)
        if tags:
            tag_objs = Tag.objects.filter(id__in=tags)
            books = books.filter(tags__in=tag_objs)
        if series:
            books = books.filter(series__in=series)
        if langs:
            books = books.filter(languages=langs)
        context["book_list"] = books.distinct()
        return render(request, 'library/results.html', context)
