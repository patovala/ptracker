#-*- coding: utf-8 -*-
#--------------------------------------------------------------------------
#
#       Colección de formularios para  A C T I V I D A D E S y P R O Y E C T O S
#
# (c) Copyright 2012 patovala@pupilabox.net.ec. All Rights Reserved. See LICENSE for details.
#--------------------------------------------------------------------------
#  author: Patricio Valarezo (c) patovala@pupilabox.net.ec
#--------------------------------------------------------------------------

#from django.forms import ModelForm, Textarea, ChoiceField, ModelMultipleChoiceField, Field, TextInput
from django.forms import ModelForm, Textarea, ChoiceField, Field, TextInput, DateField
from django.forms import extras
from django.forms.models import inlineformset_factory
from actividades.models import Actividad, RecursoXActividad, Proyecto
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
    def __init__(self, fecha_hora=None, empleado=None, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)

        if fecha_hora:
            self.fh = fecha_hora

        if empleado:
            self.fields['proyecto'].queryset = Proyecto.objects.filter(empleado=empleado)

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


class ProyectoForm(ModelForm):
    """
    ModelForm para proyectos.
    """
    porcentaje = ChoiceField(choices=[(i, "%s %%" % i) for i in range(0, 100, 10)])
    fecha_inicio = DateField(label=u'fecha inicio', input_formats=['%d/%m/%Y', '%m/%d/%Y', ], required=False, widget=extras.SelectDateWidget(attrs={'class': 'span2'}))
    fecha_fin = DateField(label=u'fecha fin', input_formats=['%d/%m/%Y', '%m/%d/%Y', ], required=False, widget=extras.SelectDateWidget(attrs={'class': 'span2'}))
    #fecha_inicio = DateTimeField('fecha_inicio',
    #    #widget=extras.SelectDateWidget(attrs={'class': 'span2'}),
    #    required=False,
    #    label=u'Fecha inicio',
    #    help_text=u'fecha en la que inicia/inició el proyecto',
    #    )

    #fecha_fin = DateTimeField('fecha_fin',
    #    #widget=extras.SelectDateWidget(attrs={'class': 'span2'}),
    #    required=False,
    #    label=u'Fecha fin',
    #    help_text=u'fecha en la que terminará el proyecto',
    #    )

    class Meta:
        model = Proyecto
        exclude = ('empleado')
        widgets = {
            'resumen': Textarea(attrs={'cols': 80, 'rows': 2, 'style': 'width:90%', 'class': 'required'}),
            'nombre': TextInput(attrs={'class': 'required', 'class': 'span4'}),
        #    'last_name': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Apellidos del Usuario", 'id': 'id_apellido'}),
        #    'email': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Email del Usuario", 'id': 'id_email'}),
        #    'password': TextInput(attrs={'data-dojo-type': "dijit.form.TextBox", 'placeholder': "Clave del Usuario", 'id': 'id_password'})
        }

    def __init__(self, *args, **kw):
        super(ProyectoForm, self).__init__(*args, **kw)
        self.fields['estado'].widget.attrs['class'] = "span2"  # hack? para formatear bien un campo

    #def clean(self):
    #    """ recargando este form por problemas con los controles de date """
    #    cleaned_data = self.cleaned_data
    #    cleaned_data['fecha_inicio'] = datetime(year=int(self.data['fecha_inicio_year']), month=int(self.data['fecha_inicio_month']), day=int(self.data['fecha_inicio_day']))
    #    cleaned_data['fecha_fin'] = datetime(year=int(self.data['fecha_fin_year']), month=int(self.data['fecha_fin_month']), day=int(self.data['fecha_fin_day']))

    #    super(ProyectoForm, self).clean()
    #    import ipdb
    #    ipdb.set_trace()
    #    return cleaned_data
