from django.contrib import admin

from .models import Templates


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'description')
    # Скрываем поле с юзером
    exclude = ['user_id']

    def save_model(self, request, obj, form, change):
        # При сохранении указываем текущего пользователя в поле user_id
        obj.user_id = request.user.id
        super().save_model(request, obj, form, change)
