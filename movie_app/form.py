from .models import Movie
from django import forms


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'actors', 'trailer_link', 'release','category']
        widgets = {
            'release': forms.DateInput(attrs={'class': 'form-control datepicker', 'type': 'date'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'poster': forms.TextInput(attrs={'class': 'form-control','type':'file'}),
            'description': forms.Textarea(attrs={'rows':3, 'class': 'form-control'}),
            'actors': forms.Textarea(attrs={'rows':3, 'class': 'form-control'}),
            'trailer_link': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'category': forms.Select(attrs={'class': 'form-control', 'type': 'text'}),
        }
