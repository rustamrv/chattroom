from django.contrib import admin
from .models import Profile, Post


@admin.register(Profile)
class ProdileAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', )


@admin.register(Post)
class Postdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
