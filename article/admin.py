from django.contrib import admin

# Register your models here.
from .models import Category, Post, Comment

# """1st method"""

# admin.site.register(Category)
# admin.site.register(Post)

"""2nd metod"""

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'tag', 'created_at', 'author')
    list_filter = ('author', 'tag', 'status', 'created_at', 'category')
    search_fields = ('title', 'tag',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'status')
    list_filter = ('created_at', 'status')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'status')
    list_filter = ('created_at', 'status')