from django import forms
from .models import Projeto

class ProjetoForm(forms.ModelForm):
    CHOICES = [(True, 'Sim'), (False, 'Não')]

    tem_cadastro_uea = forms.TypedChoiceField(
        label='Já tem cadastro na UEA?',
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False,  # Alterado para permitir valores nulos
        coerce=lambda x: x == 'True'
    )

    # Adicione o novo campo "projeto"
    projeto = forms.CharField(label='Projeto', max_length=255)

    class Meta:
        model = Projeto
        fields = ['tem_cadastro_uea', 'projeto', 'nome_projeto', 'docente_responsavel', 'discente_participante', 'matricula_discente', 'modalidade', 'vigencia_inicio', 'vigencia_fim', 'fomento', 'laboratorio']
class ExcluiRegimentoInternoForm(forms.Form):
    excluir_regimento = forms.BooleanField(required=True)
