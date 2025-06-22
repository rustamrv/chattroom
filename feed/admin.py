from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_date')
    list_filter = ('author', 'created_date')
    search_fields = ('name', 'description')
