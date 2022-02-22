# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import logging

from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class Author(models.Model):
    name = models.TextField()
    sort = models.TextField(blank=True, null=True)
    link = models.TextField()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('author-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.sort

    class Meta:
        managed = False
        db_table = 'authors'


class Comment(models.Model):
    book = models.ForeignKey("Book", db_column="book",
                             on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'comments'
        indexes = [
            models.Index(fields=["book"], name="comments_idx"),
        ]
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.text[:100]


class Data(models.Model):
    book = models.ForeignKey("Book", db_column="book", on_delete=models.CASCADE)
    format = models.TextField()
    uncompressed_size = models.IntegerField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'data'
        indexes = [
            models.Index(fields=["format"], name="formats_idx"),
            models.Index(fields=["book"], name="data_idx"),
        ]

        
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('data-detail-view', args=[str(self.id)])


class Identifier(models.Model):
    book = models.ForeignKey("Book", db_column="book", on_delete=models.CASCADE)
    type = models.TextField()
    val = models.TextField()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.val

    class Meta:
        managed = False
        db_table = 'identifiers'


class Language(models.Model):
    lang_code = models.TextField()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('language-detail-view', args=[str(self.lang_code)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.lang_code

    class Meta:
        managed = False
        db_table = 'languages'
        indexes = [
            models.Index(fields=["lang_code"], name="languages_idx"),
        ]


class Publisher(models.Model):
    name = models.TextField()
    sort = models.TextField(blank=True, null=True)
    released = models.ManyToManyField(
        "Book",
        through='BookPublisherLink',
        through_fields=('publisher', 'book'),
        related_name="released"
    )

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('publisher-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        managed = False
        db_table = 'publishers'
        indexes = [
            models.Index(fields=["name"], name="publishers_idx"),
        ]


class Rating(models.Model):
    rating = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('rating-detail-view', args=[str(self.rating)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.rating)

    class Meta:
        managed = False
        db_table = 'ratings'


class Series(models.Model):
    name = models.TextField()
    sort = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('series-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        managed = False
        db_table = 'series'
        indexes = [
            models.Index(fields=["name"], name="series_idx"),
        ]


class Tag(models.Model):
    name = models.TextField()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('tag-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    class Meta:
        managed = False
        db_table = 'tags'
        indexes = [
            models.Index(fields=["name"], name="tags_idx"),
        ]


class Book(models.Model):
    title = models.TextField()
    sort = models.TextField(blank=True, null=True)
    # This field type is a guess.
    timestamp = models.DateTimeField(blank=True, null=True)
    # This field type is a guess.
    pubdate = models.DateTimeField(blank=True, null=True)
    series_index = models.FloatField()
    author_sort = models.TextField(blank=True, null=True)
    isbn = models.TextField(blank=True, null=True)
    lccn = models.TextField(blank=True, null=True)
    path = models.TextField()
    flags = models.IntegerField()
    uuid = models.TextField(blank=True, null=True)
    has_cover = models.BooleanField(blank=True, null=True)
    last_modified = models.DateTimeField()  # This field type is a guess.
    authors = models.ManyToManyField(
        Author,
        through='BookAuthorLink',
        through_fields=('book', 'author'))
    languages = models.ManyToManyField(
        Language,
        through='BookLanguageLink',
        through_fields=('book', 'lang_code'))

    @cached_property
    def download_link(self):
        return f"{self.path}/{self.data_set.first().name}.{self.data_set.first().format.lower()}"

    @cached_property
    def cover_link(self):
        return f"{self.path}/cover.jpg"

    @cached_property
    def language(self):
        return self.languages.first()

    publishers = models.ManyToManyField(
        Publisher,
        through='BookPublisherLink',
        through_fields=('book', 'publisher'))

    @cached_property
    def publisher(self):
        return self.publishers.first()

    series = models.ManyToManyField(
        Series,
        through='BookSeriesLink',
        through_fields=('book', 'series'))

    @cached_property
    def serie(self):
        return self.series.first()

    tags = models.ManyToManyField(
        Tag,
        through='BookTagLink',
        through_fields=('book', 'tag'))
    ratings = models.ManyToManyField(
        Rating,
        through='BookRatingLink',
        through_fields=('book', 'rating'))

    @cached_property
    def rating(self):
        return self.ratings.first()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('book-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title

    class Meta:
        managed = False
        db_table = 'books'
        indexes = [
            models.Index(fields=["sort"], name="books_idx"),
            models.Index(fields=["author_sort"], name="authors_idx"),
        ]


class BookAuthorLink(models.Model):
    book = models.ForeignKey(Book, db_column="book", on_delete=models.CASCADE)
    author = models.ForeignKey(
        Author, db_column="author", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_authors_link'
        indexes = [
            models.Index(fields=["book"], name="books_authors_link_bidx"),
            models.Index(fields=["author"], name="books_authors_link_aidx"),
        ]


class BookLanguageLink(models.Model):
    book = models.ForeignKey(Book, db_column="book", on_delete=models.CASCADE)
    lang_code = models.ForeignKey(
        Language, db_column="lang_code", on_delete=models.CASCADE)
    item_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books_languages_link'
        indexes = [
            models.Index(fields=["book"], name="books_languages_link_bidx"),
            models.Index(fields=["lang_code"],
                         name="books_languages_link_aidx"),
        ]


class BookPublisherLink(models.Model):
    book = models.ForeignKey(Book, db_column="book", on_delete=models.CASCADE)
    publisher = models.ForeignKey(
        Publisher, db_column="publisher", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_publishers_link'
        indexes = [
            models.Index(fields=["book"], name="books_publishers_link_bidx"),
            models.Index(fields=["publisher"],
                         name="books_publishers_link_aidx"),
        ]


class BookRatingLink(models.Model):  # TODO add this somehow
    book = models.ForeignKey(Book, db_column="book", on_delete=models.CASCADE)
    rating = models.ForeignKey(
        Rating, db_column="rating", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_ratings_link'


class BookSeriesLink(models.Model):
    book = models.ForeignKey(Book, db_column="book", on_delete=models.CASCADE)
    series = models.ForeignKey(
        Series, db_column="series", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_series_link'
        indexes = [
            models.Index(fields=["book"], name="books_series_link_bidx"),
            models.Index(fields=["series"], name="books_series_link_aidx"),
        ]


class BookTagLink(models.Model):
    book = models.ForeignKey(Book, db_column="book", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, db_column="tag", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_tags_link'
        indexes = [
            models.Index(fields=["book"], name="books_tags_link_bidx"),
            models.Index(fields=["tag"], name="books_tags_link_aidx"),
        ]
