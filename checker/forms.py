from django import forms
from django.forms import ModelForm


class SearchForm(forms.Form):
    search_keyword = forms.CharField(label='Search', max_length=300)
