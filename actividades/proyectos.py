#-*- coding: utf-8 -*-
#--------------------------------------------------------------------------
#
#       View para P R O Y E C T O S
#
# (c) Copyright 2012 patovala@pupilabox.net.ec. All Rights Reserved. See LICENSE for details.
#--------------------------------------------------------------------------
# Un conjunto de vistas para la administración de proyectos
#--------------------------------------------------------------------------
from actividades.models import Proyecto, Empleado
from django.views.generic import list_detail
from django.http import Http404, HttpResponseRedirect
#from django.utils.html import conditional_escape as esc
from django.shortcuts import render_to_response
#from django.utils.safestring import mark_safe  # << marca una cadena como segura para ser representada
from django.template.context import RequestContext
from actividades.forms import ProyectoForm, RecursosFormSet
#auth stuff
from django.contrib.auth.decorators import login_required
#mensajes
from django.contrib import messages


@login_required
def proyectos_x_empleado(request):
    """ Obtener con generic views esta pantalla"""
    try:
        empleado = request.user.profile
    except Empleado.DoesNotExist:
        raise Http404

    # Use the object_list view for the heavy lifting.
    return list_detail.object_list(
        request,
        queryset=Proyecto.objects.all(),  # queryset=Proyecto.objects.all(),
        template_name="proyectos.html",
        #template_object_name="proyectos",  # ojo, esta variable nunca funcionó, parece que hay un bug en esto
        extra_context={"empleado": empleado, 'form_agregar_pro': ProyectoForm(), 'proyectos': Proyecto.objects.filter(empleado=empleado).all()}
    )


@login_required
def ver(request, id_proyecto):
    """ ver una proyecto via ajax """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    context = {'proyecto': proyecto}

    return render_to_response('ver_proyecto.html', context_instance=RequestContext(request, context))


@login_required
def crear(request):
    """ crear una proyecto via post """
    try:
        empleado = request.user.profile
    except Empleado.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        f = ProyectoForm(request.POST)

        if f.is_valid():
            new_proyecto = f.save(commit=False)
            new_proyecto.empleado = empleado
            # grabar el formset
            new_proyecto.save()

        else:
            messages.error(request, 'error: %s' % f.errors)

    # en el peor de los casos
    return HttpResponseRedirect("/proyectos/")


@login_required
def eliminar(request, id_proyecto):
    """ eliminar una proyecto """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    proyecto.delete()
    # en el peor de los casos
    return HttpResponseRedirect("/proyectos/calendario")


@login_required
def editar(request, id_proyecto):
    """ ver una proyecto via ajax """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    empleado = request.user.profile  # interesante esto, se debe a que el models tiene un static que genera el profile
    f = ProyectoForm(proyecto.fecha_hora, instance=proyecto)
    formset = RecursosFormSet(instance=proyecto)

    if request.method == 'POST':
        f = ProyectoForm(proyecto.fecha_hora, request.POST, instance=proyecto)
        recursos_formset = RecursosFormSet(request.POST, instance=proyecto)

        if f.is_valid() and recursos_formset.is_valid():
            #proyecto = f.save(commit=False)
            #new_proyecto.fecha_hora = f.cleaned_data['fecha_hora']
            #new_proyecto.empleado = empleado
            # grabar el formset
            proyecto.save()
            recursos_formset.save()
            messages.success(request, 'Proyecto Actualizada.')

        # en el peor de los casos
        return HttpResponseRedirect("/proyectos/calendario")

    context = {'form_agregar_act': f, 'recursos_formset': formset, 'empleado': empleado, 'proyecto': proyecto}
    return render_to_response('editar.html', context_instance=RequestContext(request, context))
