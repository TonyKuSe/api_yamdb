from import_export import resources
from reviews.models import Titles, Genre, GenreTitle, Category

class TitlesResources(resources.ModelResource):
    class Meta:
        model = Titles

class GenreResources(resources.ModelResource):
    class Meta:
        model = Genre

class GenreTitleResources(resources.ModelResource):
    class Meta:
        model = GenreTitle

class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category