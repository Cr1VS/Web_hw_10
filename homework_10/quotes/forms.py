from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Quote
from django import forms

class TagForm(ModelForm):

    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(ModelForm):

    name = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=250, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ["name", "description"]
        exclude = ["tags"]


class SearchForm(forms.Form):
    search_tags = forms.CharField(label='Search tags', max_length=50)