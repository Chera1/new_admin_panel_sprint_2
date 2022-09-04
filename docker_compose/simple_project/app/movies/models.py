import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    # auto_now_add автоматически выставит дату создания записи
    # auto_now изменятся при каждом обновлении записи
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    # Первым аргументом обычно идёт человекочитаемое название поля
    max_length = 255
    name = models.CharField(_('name'), max_length=max_length)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content\".\"genre'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'genre_id'], name='genre_film_work_idx'),
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'), null=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content\".\"person'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

    def __str__(self):
        return self.full_name


class TypeRole(models.TextChoices):
    """Наследуемый класс от TextChoices, позволяющий в поле установить выбор из перечисленных данных."""

    actor = 'actor', 'актер'
    director = 'director', 'режиссер'
    writer = 'writer', 'сценарист'


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField('role', null=True, choices=TypeRole.choices, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_idx'),
        ]


class TypeFilm(models.TextChoices):
    """Наследуемый класс от TextChoices, позволяющий в поле установить выбор из перечисленных данных."""

    movie = 'MOVIE', 'фильм'
    tv_show = 'TV_SHOW', 'шоу'


class FilmWork(UUIDMixin, TimeStampedMixin):
    max_length, max_length_cert = 255, 512
    min_value = MinValueValidator(0)
    max_value = MaxValueValidator(100)
    title = models.CharField(_('title'), max_length=max_length)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(_('rating'), validators=[min_value, max_value])
    type = models.CharField(verbose_name=_('type'), choices=TypeFilm.choices, max_length=max_length)
    certificate = models.CharField(_('certificate'), max_length=max_length_cert, blank=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружаемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content\".\"film_work'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        constraints = [
            models.UniqueConstraint(fields=['creation_date'], name='film_work_creation_date_idx'),
        ]

    def __str__(self):
        return self.title
