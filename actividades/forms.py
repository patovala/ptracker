#-*- coding: utf-8 -*-
#--------------------------------------------------------------------------
#
#       Colección de formularios para  A C T I V I D A D E S
#
#--------------------------------------------------------------------------
#  author: Patricio Valarezo (c) patovala@pupilabox.net.ec
#--------------------------------------------------------------------------

#from django.forms import ModelForm, Textarea, ChoiceField, ModelMultipleChoiceField, Field, TextInput
from django.forms import ModelForm, Textarea, ChoiceField, Field, TextInput
from django.forms.models import inlineformset_factory
from actividades.models import Actividad, RecursoXActividad
from datetime import datetime

MAX_RECURSOS = 4


class DateTimeFieldFoo(Field):
    """engañar al validate para que no chille cuando no hay fecha hora"""
    def clean(self, value):
        """ """
        return datetime.now()


class ActividadForm(ModelForm):
    """
    ModelForm para actividades.
    """
    hora = ChoiceField(choices=((6, "6am"), (7, "7am"), (8, "8am"), (9, "9am"), (10, "10am"), (11, "11am"),
      (12, "12pm"), (13, "1pm"), (14, "2pm"), (15, "3pm"), (16, "4pm"), (17, "5pm"), (18, "6pm")))
    minutos = ChoiceField(choices=((0, "00"), (15, "15min"), (30, "30min"), (45, "45min")))
    #recursos = ModelMultipleChoiceField(queryset=Recurso.objects.all())
    fecha_hora = DateTimeFieldFoo()

    class Meta:
        model = Actividad
        exclude = ('empleado', 'recursos')
        widgets = {
                'objetivos': Textarea(attrs={'cols': 80, 'rows': 2, 'style': 'width:90%', 'class': 'required'}),
                'actividad': TextInput(attrs={'class': 'required'}),
        #    'first_name': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Nombres del Usuario", 'id': 'id_nombre'}),
        #    'last_name': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Apellidos del Usuario", 'id': 'id_apellido'}),
        #    'email': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Email del Usuario", 'id': 'id_email'}),
        #    'password': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Clave del Usuario", 'id': 'id_password'})
        }

    # Overriding __init__ here allows us to provide initial
    # data for 'toppings' field
    def __init__(self, fecha_hora=None, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)

        if fecha_hora:
            self.fh = fecha_hora

    def clean(self):
        """ recargando esta vaina"""
        cleaned_data = self.cleaned_data
        fh = self.fh
        self.fh = datetime(year=fh.year, month=fh.month, day=fh.day, hour=int(self.cleaned_data['hora']), minute=int(self.cleaned_data['minutos']))
        cleaned_data['fecha_hora'] = self.fh

        super(ActividadForm, self).clean()

        return cleaned_data


class RecursoModelForm(ModelForm):
    """
        Un modelform para recursos
    """
    def __init__(self, *args, **kwargs):
        super(RecursoModelForm, self).__init__(*args, **kwargs)
        self.fields['cant'].widget.attrs['class'] = 'span1'

RecursosFormSet = inlineformset_factory(Actividad, RecursoXActividad, form=RecursoModelForm, can_delete=False, extra=MAX_RECURSOS)
