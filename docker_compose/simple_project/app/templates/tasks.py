from requests import post

from celery import shared_task

from movies.models import FilmWork


@shared_task
def send_mail_massage(*args, **kwargs):
    # Тут будет отправка в API
    request = post('url', json=kwargs)
    return 'Successful! ' + str(request.status_code)


@shared_task
def most_popular_films(*args, **kwargs):
    list_of_films = FilmWork.objects.filter(rating__gte=6)
    ids_films = [each_film.id for each_film in list_of_films]
    kwargs['context'].update(movies=ids_films)
    # Тут будет отправка в API
    request = post('url', json=kwargs)
    result = request.status_code
    return result

