from django.forms import ModelForm, CharField, TextInput
from django.forms import ModelChoiceField
from django import forms


from .models import Tag, Quote, Author


class TagForm(ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ["name"]



class QuoteForm(ModelForm):
    name = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all(), empty_label=None, required=True)

    class Meta:
        model = Quote
        fields = ["name", "author"]
        exclude = ["tags"]


class SearchForm(forms.Form):
    search_tags = forms.CharField(label="Search tags", max_length=50)


class AuthorForm(ModelForm):
    fullname = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    born_date = CharField(min_length=10, max_length=200, required=True, widget=TextInput())
    born_location = CharField(min_length=10, max_length=250, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=2000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
