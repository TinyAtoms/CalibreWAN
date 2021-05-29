# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import  Layout, Fieldset, Submit
# from crispy_forms.bootstrap import Div, InlineField, InlineRadios
from dal import autocomplete
from django import forms

from .models import *

AND_OR = [
    (0, 'OR'),
    (1, "AND")
]


class BookFilterForm(forms.Form):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='author-autocomplete'),
        required=False
    )
    authors_andor = forms.ChoiceField(
        label="author behaviour",
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
    tags_andor = forms.ChoiceField(
        label="tags behaviour",
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
    series_andor = forms.ChoiceField(
        label="series behaviour",
        initial=0,
        choices=AND_OR, required=False,
        widget=forms.RadioSelect)

    langs = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        widget=autocomplete.ModelSelect2(url='lang-autocomplete'),
        required=False
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Div(
    #             Div('authors', css_class='col-md-6', ),
    #             InlineRadios('authors_andor', css_class='col-md-6', ),
    #             css_class='row',
    #         ),
    #         Div(
    #             Div('tags', css_class='col-md-6', ),
    #             InlineRadios('tags_andor', css_class='col-md-6', ),
    #             css_class='row',
    #         ),
    #         Div(
    #             Div('series', css_class='col-md-6', ),
    #             InlineRadios('series_andor', css_class='col-md-6', ),
    #             css_class='row',
    #         ),
    #         Div("langs", css_class="col-md-6")
    #     )
    #
    #     self.helper.form_id = 'filter'
    #     self.helper.form_class = 'blueForms'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = 'filter'
    #
    #     self.helper.add_input(Submit('submit', 'Submit'))



class SearchForm(forms.Form):
    # title = forms.CharField(label="Title", max_length=200, required=False)
    # author = forms.CharField(label='Author', max_length=100, required=False)
    # identifier = forms.CharField(label='Identifier(ISBN, Google-id, amazon id)', max_length=20, required=False)
    generic = forms.CharField(label='All', max_length=100, required=False)