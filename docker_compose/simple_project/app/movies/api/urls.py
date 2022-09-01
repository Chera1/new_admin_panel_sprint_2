from django.urls import path, include


urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
