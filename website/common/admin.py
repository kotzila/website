from django.contrib import admin
from common.models import Genre, KeyWord, ProductionCompany, Country


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductionCompany)
class ProductionCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
