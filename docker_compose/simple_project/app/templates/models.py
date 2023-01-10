from django.db import models
from django.utils.translation import gettext_lazy as _

from movies.models import TimeStampedMixin, UUIDMixin


class Templates(UUIDMixin, TimeStampedMixin):
    max_length = 255

    name = models.CharField(_('name'), max_length=max_length)
    description = models.TextField(_('description'), blank=True)
    user_id = models.IntegerField(_('user'), blank=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружаемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='templates/jinja2/')

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content\".\"templates'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def __str__(self):
        return self.name
