#-*- coding: utf-8 -*-
#--------------------------------------------------------------------------
#
#       View para A C T I V I D A D E S
#
#--------------------------------------------------------------------------
# Un conjunto de vistas para la administración de actividades
#--------------------------------------------------------------------------
from actividades.models import Actividad, Empleado
from django.views.generic import list_detail
from django.http import Http404, HttpResponseRedirect
from django.utils.html import conditional_escape as esc
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe  # << marca una cadena como segura para ser representada
from django.template.context import RequestContext
from actividades.forms import ActividadForm, RecursosFormSet
#auth stuff
from django.contrib.auth.decorators import login_required
#mensajes
from django.contrib import messages

# calendario stuff
from calendar import LocaleHTMLCalendar
from datetime import date, datetime
from itertools import groupby
# settings
import settings


def actividades_x_empleado(request):
    """ Listar las actividades de un empleado """
    try:
        #empleado = Empleado.objects.get(user__username=username)
        empleado = request.user.profile
    except Empleado.DoesNotExist:
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_list(
        request,
        queryset=Actividad.objects.filter(empleado=empleado),
        template_name="master.html",
        template_object_name="actividades",
        extra_context={"empleado": empleado}
    )


# Una clase que maneja calendarios
class ActividadCalendar(LocaleHTMLCalendar):

    def __init__(self, actividades):
        super(ActividadCalendar, self).__init__(locale=settings.LOCALE)
        self.actividades = self.group_by_day(actividades)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            day_href = """<div class="addact"><span class="label label-success">%d</span>
                    <div class="bar hide">
                        <div class="toolbar">
                            <a class="btn btn-primary btn-mini frmaa" href="/actividades/crear/%d/%d/%s">agregar actividad</a>
                        </div>
                    </div></div>
            """ % (day, day, self.month, self.year)

            if date.today() == date(self.year, self.month, day):
                cssclass += ' hoy'
            if day in self.actividades:
                cssclass += ' filled'
                body = ['<dl>']
                for actividad in self.actividades[day]:
                    body.append('<dt>%s</dt>' % actividad.fecha_hora.strftime(u"%H:%M"))
                    body.append('<dd><i class="icon-upload"></i><a class="veract" href="/actividades/ver/%s">' % actividad.id)
                    body.append(esc(actividad.actividad))
                    body.append('</a></<dd>')
                body.append('</dl>')
                #body.append('<a class="btn btn-mini formact" href="#">agregar</a>')
                return self.day_cell(cssclass, '%s %s' % (day_href, ''.join(body)))
            return self.day_cell(cssclass, day_href)
        return self.day_cell('noday', '&nbsp;')

    #def formatmonth(self, year, month):
    #    self.year, self.month = year, month
    #    return super(ActividadCalendar, self).formatmonth(year, month)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = theyear, themonth

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="table-bordered table-striped">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def group_by_day(self, actividades):
        field = lambda actividad: actividad.fecha_hora.day
        return dict(
            [(day, list(items)) for day, items in groupby(actividades, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


@login_required
def calendario(request, year=None, month=None):
    """ Un calendario con las actividades """
    empleado = request.user.profile  # interesante esto, se debe a que el models tiene un static que genera el profile

    if year == None and month == None:
        year = date.today().year
        month = date.today().month
    else:
        year = int(year)
        month = int(month)

    prev_month = month - 1
    prev_year = year

    if prev_month < 1:
        prev_year = prev_year - 1
        prev_month = 12

    prev_nombre = date(year=prev_year, month=prev_month, day=1).strftime("%B")

    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_year = next_year + 1
        next_month = 1

    next_nombre = date(year=next_year, month=next_month, day=1).strftime("%B")

    mis_actividades = Actividad.objects.order_by('fecha_hora').filter(fecha_hora__year=year, fecha_hora__month=month)

    cal = ActividadCalendar(mis_actividades).formatmonth(year, month)
    context = {'calendario': mark_safe(cal),
                'form_agregar_act': ActividadForm(),
                'recursos_formset': RecursosFormSet(),
                'empleado': empleado,
                'prev_link': (prev_year, prev_month, prev_nombre),
                'next_link': (next_year, next_month, next_nombre),
                }

    return render_to_response('calendario.html', context_instance=RequestContext(request, context))


@login_required
def ver(request, id_actividad):
    """ ver una actividad via ajax """
    actividad = Actividad.objects.get(pk=id_actividad)
    context = {'actividad': actividad}

    return render_to_response('ver.html', context_instance=RequestContext(request, context))


@login_required
def crear(request, dia, mes, anio):
    """ crear una actividad via post """
    fecha = datetime(year=int(anio), month=int(mes), day=int(dia))
    empleado = Empleado.objects.get(pk=1)

    if request.method == 'POST':
        f = ActividadForm(fecha, request.POST)

        if f.is_valid():
            new_actividad = f.save(commit=False)
            #new_actividad.fecha_hora = f.cleaned_data['fecha_hora']
            new_actividad.empleado = empleado
            # grabar el formset
            new_actividad.save()
            recursos_formset = RecursosFormSet(request.POST, instance=new_actividad)
            recursos_formset.save()

    # en el peor de los casos
    return HttpResponseRedirect("/actividades/calendario")


@login_required
def eliminar(request, id_actividad):
    """ eliminar una actividad """

    actividad = Actividad.objects.get(pk=id_actividad)
    actividad.delete()
    # en el peor de los casos
    return HttpResponseRedirect("/actividades/calendario")


@login_required
def editar(request, id_actividad):
    """ ver una actividad via ajax """
    actividad = Actividad.objects.get(pk=id_actividad)
    empleado = request.user.profile  # interesante esto, se debe a que el models tiene un static que genera el profile
    f = ActividadForm(actividad.fecha_hora, instance=actividad)
    formset = RecursosFormSet(instance=actividad)

    if request.method == 'POST':
        f = ActividadForm(actividad.fecha_hora, request.POST, instance=actividad)
        recursos_formset = RecursosFormSet(request.POST, instance=actividad)

        if f.is_valid() and recursos_formset.is_valid():
            #actividad = f.save(commit=False)
            #new_actividad.fecha_hora = f.cleaned_data['fecha_hora']
            #new_actividad.empleado = empleado
            # grabar el formset
            actividad.save()
            recursos_formset.save()
            messages.success(request, 'Actividad Actualizada.')

        # en el peor de los casos
        return HttpResponseRedirect("/actividades/calendario")

    context = {'form_agregar_act': f, 'recursos_formset': formset, 'empleado': empleado, 'actividad': actividad}
    return render_to_response('editar.html', context_instance=RequestContext(request, context))
