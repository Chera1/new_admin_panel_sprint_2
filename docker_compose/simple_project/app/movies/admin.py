from django.contrib import admin

from .models import Genre, FilmWork, GenreFilmWork, PersonFilmWork, Person


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'description')

    # Поиск по полям
    search_fields = ('name', 'id')


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ['genre', ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('full_name',)

    # Поиск по полям
    search_fields = ('full_name', 'id')


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ['person', ]


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')
    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (super().get_queryset(request).prefetch_related(*self.list_prefetch_related))
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'

    # Фильтрация в списке
    list_filter = ('type', 'creation_date', 'genres')

    # Поиск по полям
    search_fields = ('title', 'description', 'id')