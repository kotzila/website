from django.conf.urls import url
from dal import autocomplete
from stars.models import Star
from common.models import Country, ProductionCompany, KeyWord, Genre
from movies.models import Movie
from images.models import Image

urlpatterns = [
    # autocomplete
    url('autocomplete/star/$', autocomplete.Select2QuerySetView.as_view(model=Star, create_field='name'),
        name='star_autocompleate'),
    url('autocomplete/country/$', autocomplete.Select2QuerySetView.as_view(model=Country, create_field='name'),
        name='country_autocomplete'),
    url('autocomplete/company/$',
        autocomplete.Select2QuerySetView.as_view(model=ProductionCompany, create_field='name'),
        name='company_autocomplete'),
    url('autocomplete/keyword/$', autocomplete.Select2QuerySetView.as_view(model=KeyWord, create_field='name'),
        name='keyword_autocomplete'),
    url('autocomplete/genres/$', autocomplete.Select2QuerySetView.as_view(model=Genre, create_field='name'),
        name='genre_autocomplete'),
    url('autocomplete/movie/$', autocomplete.Select2QuerySetView.as_view(model=Movie), name='movie_autocomplete'),
    url('autocomplete/images/$', autocomplete.Select2QuerySetView.as_view(model=Image), name='image_autocomplete'),
]

