from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser


class Titles(models.Model):
    name = models.CharField('Название произведения',
                            max_length=200,
                            db_index=True)
    year = models.IntegerField('Год написания')
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='Категория')
    description = models.TextField('Описание',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    genre = models.ManyToManyField('Genre',
                                   related_name='titles',
                                   verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название',
                            max_length=256)
    slug = models.SlugField(unique=True,
                            max_length=50,
                            db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug жанра',
                            unique=True,
                            max_length=50,
                            db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Titles,
                                 on_delete=models.CASCADE,
                                 related_name='genre_title')
    genre_id = models.ForeignKey(Genre,
                                 on_delete=models.CASCADE,
                                 related_name='genre_title')

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Reviews(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField('Оценка', validators=[MinValueValidator(1),
                                                      MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name


class Comments(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.name
