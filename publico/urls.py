from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('geral/', views.geral , name='geral'),
    path('view/<int:laboratorio_id>/', views.view, name='view')
]
# if settings.DEBUG:
urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
