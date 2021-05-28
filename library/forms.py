from dal import autocomplete
from django import forms

from .models import *

AND_OR = [
    (0, 'OR'),
    (1, "AND")
]


class BookFilterForm(forms.Form):
    title = forms.CharField(label="Title", required=False)
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='author-autocomplete'),
        required=False
    )
    authors_andor = forms.ChoiceField(label="author behaviour", choices=AND_OR, required=True, widget=forms.RadioSelect)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        required=False
    )
    tags_andor = forms.ChoiceField(label="tags behaviour", choices=AND_OR, required=True, widget=forms.RadioSelect)

    series = forms.ModelMultipleChoiceField(
        queryset=Series.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='series-autocomplete'),
        required=False
    )
    series_andor = forms.ChoiceField(label="series behaviour", choices=AND_OR, required=True, widget=forms.RadioSelect)

    langs = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=autocomplete.ModelSelect2(url='lang-autocomplete'),
        required=False
    )
