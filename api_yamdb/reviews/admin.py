from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from reviews.models import (Title, Genre, GenreTitle, Category,
                            Review, Comments)


@admin.register(Title)
class TitleAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'description')


@admin.register(Genre)
class GenreAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'title_id', 'genre_id')


@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Review)
class ReviewsAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score')


@admin.register(Comments)
class CommentsAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'text', 'author', 'review')
