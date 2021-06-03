import datetime

from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError

from .models import *

AND_OR = [
    (0, 'OR'),
    (1, "AND")
]
RATING_CHOICE = [(i, i) for i in range(11)]
YEAR_CHOICE = [i for i in range(2022, 1970, -1)]


class BookFilterForm(forms.Form):
    """
    form for advanced filtering, Booklist and various X_detail views
    """
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='author-autocomplete'),
        required=False
    )
    authors_andor = forms.TypedChoiceField(
        label="author behaviour",
        coerce=int,
        choices=AND_OR,
        initial=0,
        required=False,
        widget=forms.RadioSelect)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='tag-autocomplete',
            forward=['authors']),
        required=False
    )
    tags_andor = forms.TypedChoiceField(
        label="tags behaviour",
        coerce=int,
        initial=0,
        choices=AND_OR, required=False,
        widget=forms.RadioSelect)

    series = forms.ModelMultipleChoiceField(
        queryset=Series.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='series-autocomplete',
            forward=['authors', "tags"]),
        required=False
    )
    series_andor = forms.TypedChoiceField(
        label="series behaviour",
        initial=0,
        coerce=int,
        choices=AND_OR, required=False,
        widget=forms.RadioSelect)

    languages = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=autocomplete.ModelSelect2(url='lang-autocomplete'),
        required=False
    )
    ratings__rating__gte = forms.TypedChoiceField(
        label="rating",
        choices=RATING_CHOICE,
        coerce=int,
        initial=RATING_CHOICE[0])
    pubdate__gte = forms.IntegerField(label="smallest publishing year", required=False)
    pubdate__lte = forms.IntegerField(label="biggest publishing year", required=False)
    timestamp__gte = forms.DateTimeField(label="begin date range added to calibre", required=False,
                                         widget=forms.SelectDateWidget(years=YEAR_CHOICE))
    timestamp__lte = forms.DateTimeField(label="end date range added to calibre", required=False,
                                         widget=forms.SelectDateWidget(years=YEAR_CHOICE))

    def clean_pubdate__gte(self):
        """
        transform year integer to date object
        :return: date object
        """
        data = self.cleaned_data['pubdate__gte']
        if not data:
            return None
        try:
            data = datetime.date(data, 1, 1)
        except ValueError:
            raise ValidationError("Invalid year.")
        return data

    def clean_pubdate__lte(self):
        """
         transform year integer to date object
         :return: date object
         """
        data = self.cleaned_data['pubdate__lte']
        if not data:
            return None
        try:
            data = datetime.date(data, 12, 31)
        except ValueError:
            raise ValidationError("Invalid year.")
        return data


class SearchForm(forms.Form):
    # title = forms.CharField(label="Title", max_length=200, required=False)
    # author = forms.CharField(label='Author', max_length=100, required=False)
    # identifier = forms.CharField(label='Identifier(ISBN, Google-id, amazon id)', max_length=20, required=False)
    generic = forms.CharField(label='All', max_length=100, required=False)
