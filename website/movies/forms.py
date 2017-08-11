from django import forms
from dal import autocomplete
from movies.models import Movie, Video


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ()
        widgets = {
            'production_companies': autocomplete.ModelSelect2Multiple(url='company_autocomplete'),
            'production_countries': autocomplete.ModelSelect2Multiple(url='country_autocomplete'),
            'keywords': autocomplete.ModelSelect2Multiple(url='keyword_autocomplete'),
            'genres': autocomplete.ModelSelect2Multiple(url='genre_autocomplete'),
            'poster': autocomplete.ModelSelect2(url='image_autocomplete'),
            'images': autocomplete.ModelSelect2Multiple(url='image_autocomplete')
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('order', )

        widgets = {
            'movie': autocomplete.ModelSelect2(url='movie_autocomplete',
                                              forward=('owner',))
        }
