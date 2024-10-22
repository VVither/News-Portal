from django.contrib import admin

from .models import Author, BadWord, Category, Comment, Post, PostCategory

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(BadWord)
