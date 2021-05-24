from django.contrib import admin
from .models import Author, Book, Language, Publisher, Series, Tag
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (["name"])

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (["id", "lang_code"])

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = (["id","name"])

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (["id","name"])

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (["id","name"])

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (["id","title", "author_sort"])