from ninja import NinjaAPI
from datetime import datetime
from library import models
from .models import  BookProgress
from ninja.security import django_auth
from ninja import Schema

def serialize_author_qs(qs):
    authors = list(qs.values("id", "name"))
    for i, author in enumerate(authors):
        authors[i]["link"] = f"/apiv1/author/{author['id']}"
    return authors

def serialize_author(id: int):
    return models.Author.objects.get(id=id)


def serialize_book_qs(qs):
    books =  list(qs.values("id", "title"))
    for i, book in enumerate(books):
        books[i]["link"] = f"/apiv1/book/{book['id']}"
    return books

def serialize_book(id: int):
    book = models.Book.objects.get(id=id)
    return book
    

def serialize_identifier_qs(qs):
    return list(qs.values("type", "val"))

def serialize_language_qs(qs):
    langs =  list(qs.values("id", "lang_code"))
    for i, lang in enumerate(langs):
        langs[i]["link"] = f"/apiv1/language/{lang['id']}"
    return langs

def serialize_language(id: int):
    return models.Language.objects.get(id=id)

def serialize_publisher_qs(qs):
    pubs =  list(qs.values("id", "name"))
    for i, pub in enumerate(pubs):
        pubs[i]["link"] = f"/apiv1/publisher/{pub['id']}"
    return pubs

def serialize_publisher(id: int):
    return models.Publisher.objects.get(id=id)

def serialize_rating_qs(qs):
    ratings =  list(qs.values("id", "rating"))
    for i, rating in enumerate(ratings):
        ratings[i]["link"] = f"/apiv1/rating/{rating['id']}"
    return ratings

def serialize_rating(id: int):
    return models.Rating.objects.get(id=id)


def serialize_series_qs(qs):
    series =  list(qs.values("id", "name"))
    for i, serie in enumerate(series):
        series[i]["link"] = f"/apiv1/serie/{serie['id']}"
    return series

def serialize_series(id: int):
    return models.Series.objects.get(id=id)

def serialize_tag_qs(qs):
    tags =  list(qs.values("id", "name"))
    for i, tag in enumerate(tags):
        tags[i]["link"] = f"/apiv1/tag/{tag['id']}"
    return tags

def serialize_tag(id: int):
    return models.Tag.objects.get(id=id)





api = NinjaAPI(version="1.0", csrf=True) 







@api.get("/", auth=django_auth)
def root(request):
    response = {
        "authors" : "/apiv1/authors",
        "books" : "/apiv1/books",
        "languages" : "/apiv1/languages",
        "publishers" : "/apiv1/publishers",
        "ratings" : "/apiv1/ratings",
        "series" : "/apiv1/series",
        "tags" :"/apiv1/tags"
    }
    return response

@api.get("/authors", auth=django_auth)
def authors(request):
    response = {
        "authors" : serialize_author_qs(models.Author.objects.all())
    }
    return response

@api.get("/author/{author_id}", auth=django_auth)
def author(request, author_id: int):
    author = serialize_author(author_id)
    response = {
        "id" : author.id,
        "name" : author.name,
        "books" : serialize_book_qs(models.Book.objects.filter(authors__id=author_id))
        
    }
    return response


@api.get("/languages", auth=django_auth)
def languages(request):
    response = {
        "languages" : serialize_language_qs(models.Language.objects.all())
    }
    return response

@api.get("/language/{lang_id}", auth=django_auth)
def language(request, lang_id: int):
    lang = serialize_language(lang_id)
    response = {
        "id" : lang.id,
        "lang" : lang.lang_code,
        "books" : serialize_book_qs(models.Book.objects.filter(languages__id=lang_id))
        
    }
    return response


@api.get("/publishers", auth=django_auth)
def publishers(request):
    response = {
        "publishers" : serialize_publisher_qs(models.Publisher.objects.all())
    }
    return response

@api.get("/publisher/{pub_id}", auth=django_auth)
def publisher(request, pub_id: int):
    pub = serialize_publisher(pub_id)
    response = {
        "id" : pub.id,
        "publisher" : pub.name,
        "books" : serialize_book_qs(models.Book.objects.filter(publishers__id=pub_id))
        
    }
    return response


@api.get("/ratings", auth=django_auth)
def ratings(request):
    response = {
        "ratings" : serialize_rating_qs(models.Rating.objects.all())
    }
    return response

@api.get("/rating/{rating_id}", auth=django_auth)
def rating(request, rating_id: int):
    rating = serialize_rating(rating_id)
    response = {
        "id" : rating.id,
        "rating" : rating.rating,
        "books" : serialize_book_qs(models.Book.objects.filter(ratings__id=rating_id))
        
    }
    return response


@api.get("/series", auth=django_auth)
def series(request):
    response = {
        "series" : serialize_series_qs(models.Series.objects.all())
    }
    return response

@api.get("/serie/{series_id}", auth=django_auth)
def serie(request, series_id: int):
    series = serialize_series(series_id)
    response = {
        "id" : series.id,
        "series" : series.name,
        "books" : serialize_book_qs(models.Book.objects.filter(series__id=series_id))
        
    }
    return response

@api.get("/tags", auth=django_auth)
def tags(request):
    response = {
        "tags" : serialize_tag_qs(models.Tag.objects.all())
    }
    return response

@api.get("/tag/{tag_id}", auth=django_auth)
def tag(request, tag_id: int):
    tag = serialize_tag(tag_id)
    response = {
        "id" : tag.id,
        "tag" : tag.name,
        "books" : serialize_book_qs(models.Book.objects.filter(tag__id=tag_id))
        
    }
    return response

@api.get("/book/{book_id}", auth=django_auth)
def book(request, book_id: int):
    book = serialize_book(book_id)
    formats = []
    for f in book.data_set.all(): # maybe data_set
        formats.append({
            "url" : f"/UserLibrary/{book.path}/{f.name}.{f.format.lower()}",
            "format" : f.format.lower()
        })
    response = {
        "title" : book.title,
        "authors" : serialize_author_qs(book.authors),
        "languages" : serialize_language_qs(book.languages), 
        "publishers" : serialize_publisher_qs(book.publishers),
        "series" : serialize_series_qs(book.series),
        "tags" : serialize_tag_qs(book.tags),
        "identifiers" : serialize_identifier_qs(book.identifier_set.all()), # maybe identifier_set
        "cover" : f"/UserLibrary/{book.path}/cover.jpg",
        "formats" : formats
    }
    return response


def get_bookprogress(book: int, user: str ):
    try:
        progress = BookProgress.objects.get(user=user, book=book)
        return progress.progress
    except BookProgress.DoesNotExist:
        return 0


@api.get("/bookprogress/{book}/{user}", auth=django_auth)
def bookprogress_GET(request, book: int, user: str):
    progress = get_bookprogress(book, user)
    response = {
        "book" : book,
        "user" : user,
        "progress" : progress 
    }
    return response


def create_or_update_bp(book: int, user: str, progress:str):
    try:
        bp = BookProgress.objects.get(user=user, book=book)
        bp.progress = progress
        bp.save()
    except BookProgress.DoesNotExist:
        bp = BookProgress.objects.create(book=book, user=user, progress=progress)
    return {
        "book" : bp.book,
        "user" : bp.user,
        "progress" : bp.progress 
    }
 

class BP(Schema):
    book: int
    user: str
    progress: str


# This needs to be PUT, and not doing so is a security risk
@api.put("/bookprogress/", auth=django_auth)
def bookprogress_PUT(request, item: BP):
    return create_or_update_bp(item.book, item.user, item.progress)

# # This needs to be PUT, and not doing so is a security risk
# @api.get("/bookprogress/{book}/{user}/{progress}", auth=django_auth)
# def bookprogress_cancer_GET(request, book: int, user: str, progress: str):
#     return create_or_update_bp(book, user, progress)