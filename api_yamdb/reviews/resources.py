from import_export import resources

from reviews.models import (Category, Comments, Genre, GenreTitle,
                            Review, Title)


class TitleResources(resources.ModelResource):
    class Meta:
        model = Title


class GenreResources(resources.ModelResource):
    class Meta:
        model = Genre


class GenreTitleResources(resources.ModelResource):
    class Meta:
        model = GenreTitle


class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category


class ReviewResources(resources.ModelResource):
    class Meta:
        model = Review


class CommentsResources(resources.ModelResource):
    class Meta:
        model = Comments
