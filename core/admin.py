from django.contrib import admin

# from .models import Composicao
from .models import AtoNormativ
from .models import Autoridade
from .models import Composicao
from .models import BoletimGerado

# class AutoridadesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'nome')
#     # list_display_links = ('id', 'nome')
#     list_filter = ('nome')
#     list_per_page = 10
#     search_fields = ('nome')

class Atodmin(admin.ModelAdmin):
    list_display = ('id', ' texto_normativo','ementa')
    # list_display_links = ('id', 'nome')
    list_filter = (' texto_normativo')
    list_per_page = 10
    search_fields = (' texto_normativo')
    

admin.site.register(BoletimGerado)
admin.site.register(AtoNormativ)
admin.site.register(Autoridade)
admin.site.register(Composicao)
# admin.site.register(Composicao)
