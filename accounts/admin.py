from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProdileAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', )
