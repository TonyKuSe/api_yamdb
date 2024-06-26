from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from reviews.validates import validate_year

User = get_user_model()

MIN_SCORE = 1
MAX_SCORE = 10


class Title(models.Model):
    name = models.CharField('Название произведения',
                            max_length=200,
                            db_index=True)
    year = models.PositiveSmallIntegerField('Год написания',
                                            db_index=True,
                                            validators=[validate_year])
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='title',
                                 verbose_name='Категория')
    description = models.TextField('Описание',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    genre = models.ManyToManyField('Genre',
                                   related_name='title',
                                   verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year']

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
        ordering = ['name']

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
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='genre_title')
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              related_name='genre_title')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(Title, verbose_name='titles',
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'Оценка', validators=[MinValueValidator(MIN_SCORE),
                              MaxValueValidator(MAX_SCORE)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-score', '-pub_date')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review')]

    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        ordering = ('review', '-pub_date')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text[:15]
