from django.contrib.auth.backends import ModelBackend
from .models import OracleUser, Usuariopadaces, Padaces


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = OracleUser.objects.get(USER_LDAP=username, ATIVO='S')

            # Verifica se o usuário possui os PADACES corretos (697 ou 698)
            padaces_697_698 = Padaces.objects.filter(PADACES__in=['697', '698'])
            if Usuariopadaces.objects.filter(USUARIO=user, PADACES__in=padaces_697_698).exists():
                return user
        except OracleUser.DoesNotExist:
            return None
