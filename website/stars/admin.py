from django.contrib import admin
from stars.models import Star


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    pass
