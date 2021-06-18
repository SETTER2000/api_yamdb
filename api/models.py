from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

#
# class Genre(models.Model):
#     """Жанр."""
#     name = models.CharField(
#         'название жанра',
#         max_length=200,
#         help_text='Придумайте краткое название для жанра произведений')
#     slug = models.SlugField(
#         # unique=True,
#         blank=True,
#         null=True,
#         max_length=100,
#         verbose_name='url (slug)',
#         help_text='Краткое, уникальное слово, которое будет '
#                   'видно в ссылке на страницу жанра (часть URL)')
#
#     class Meta:
#         db_table = 'genres_title'
#         verbose_name = 'genre'
#         verbose_name_plural = 'Жанр'
#
#
# class Category(models.Model):
#     """Категория."""
#     name = models.CharField(
#         'название категории',
#         max_length=200,
#         help_text='Придумайте краткое название категории произведений')
#     slug = models.SlugField(
#         # unique=True,
#         blank=True,
#         null=True,
#         max_length=100,
#         verbose_name='url (slug)',
#         help_text='Краткое, уникальное слово, которое будет '
#                   'видно в ссылке на страницу категории (часть URL)')
#
#     class Meta:
#         db_table = 'categories_title'
#         verbose_name = 'category'
#         verbose_name_plural = 'Категория'
#
#
# class Title(models.Model):
#     """Произведения."""
#     name = models.TextField()
#
#     year = models.DateTimeField(
#         'Год публикации', auto_now_add=True
#     )
#
#     description = models.TextField(
#         'описание',
#         blank=True,
#         null=True,
#         help_text='Опишите жанр так, чтобы пользователь мог легко  '
#                   'определиться с выбором жанра для произведения.')
#
#     genre = models.ForeignKey(
#         'Genre',
#         models.SET_NULL,
#         blank=True,
#         null=True,
#         verbose_name='жанр',
#         help_text='Жанр произведения.',
#         related_name='genre_titles')
#
#     category = models.ForeignKey(
#         'Category',
#         models.SET_NULL,
#         blank=True,
#         null=True,
#         verbose_name='категория',
#         help_text='Категория произведения.',
#         related_name='category_titles')
#
#     class Meta:
#         db_table = 'titles_title'
#         ordering = ('-year',)
#         verbose_name = 'title'
#         verbose_name_plural = 'произведения'


class User(models.Model):
    """Custom User model.

    User has roles:

    anonymous - can only read,
    user - can read and public reviews, rating; can raed and edit how own
           comments and rating
    moderator - like user, but also can delete or edit comments and reviews,
    admin -has all rules, can get rules to users
    """

    ROLE_CHOICES = [
        ('anon', 'Anonymous'),
        ('user', 'user'),
        ('moder', 'moderator'),
        ('admin', 'admin'),
    ]

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=30, unique=True, validators=[username_validator]
    )
    email = models.EmailField(
        _('email address'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    description = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    def __str__(self):
        return f'{self.username}, has a {self.role} role'

    class Meta:
        verbose_name = 'User'


class Title(models.Model):
    """Название произведения."""
    name = models.TextField(
        'Название произведения',
        max_length=200,
        help_text='Введите название произведения',
    )
    year = models.DecimalField(
        'Год выпуска',
        max_digits=4,
        decimal_places=0,
        null=True,
        blank=True,
        help_text='Год выпуска'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        help_text='Введите описание вашего произведения.'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='Category',
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Жанр',
        related_name='Genre',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('category',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Category(models.Model):
    """Тип произведения."""
    name = models.CharField(
        'Категория произведения',
        max_length=200,
        unique=True,
        help_text='Введите категорию произведения.'
    )
    slug = models.SlugField(
        'URL',
        unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Название жанра."""
    name = models.TextField(
        'Название жанра', max_length=200, help_text='Введите название жанра'
    )
    slug = models.SlugField('URL', unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Review(models.Model):
    """Отзыв с оценкой (рейтингом)."""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.SmallIntegerField(10)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        db_table = 'reviews_review'
        ordering = ('-pub_date',)
        verbose_name = 'review'
        verbose_name_plural = 'отзывы'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['author'],
        #         name='unique user_following',
        #     )
        # ]


class Comment(models.Model):
    """Комментарий к отзыву."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произвидение',
        help_text='Произведение интелектуальное.',
        related_name='title')
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв',
        help_text='Отзыв на котоорый сделан комментарий.',
        related_name='review')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'comment'
        verbose_name_plural = 'комментарии'
