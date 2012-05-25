from actividades.models import Lugar, Recurso, Actividad, Proyecto, Empleado

from django.contrib import admin

#class EgresadoAdmin(admin.ModelAdmin):
#    """wrapper para que no presente en el admin algunas cosas"""
#    fields = ('cedula','nombres','apellidos')
#
#class DocenteAdmin(admin.ModelAdmin):
#    """wrapper para administracion de docentes que no pida usuario al crear el docente"""
#    fields = ('cedula','titulo','nombres','apellidos','user')
#
#admin.site.register(Docente, DocenteAdmin)
#admin.site.register(Egresado, EgresadoAdmin)
#admin.site.register(SegTesParam)
admin.site.register(Lugar)
admin.site.register(Recurso)
admin.site.register(Actividad)
admin.site.register(Proyecto)
admin.site.register(Empleado)
