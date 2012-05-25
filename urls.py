from django.conf.urls.defaults import patterns, include, url
from actividades.models import Actividad
from django.conf import settings
from django.contrib.auth.views import login  # , logout


# PV importar renderizador estanda de vistas
# https://docs.djangoproject.com/en/dev/topics/generic-views/

from django.views.generic import list_detail
#from actividades.views import actividades_x_empleado

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

actividades_x_empleado = {
    "queryset": Actividad.objects.all(),
    "template_name": "master.html",
}


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ptrack.views.home', name='home'),
    # url(r'^ptrack/', include('ptrack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^actividades/$', list_detail.object_list, actividades_x_empleado),
    (r'^actividades/calendario$', 'ptrack.actividades.views.calendario'),
    (r'^actividades/calendario/(\d{4})/(\d{2})/$', 'ptrack.actividades.views.calendario'),
    (r'^actividades/ver/(\d+)$', 'ptrack.actividades.views.ver'),
    (r'^actividades/eliminar/(\d+)$', 'ptrack.actividades.views.eliminar'),
    (r'^actividades/editar/(\d+)$', 'ptrack.actividades.views.editar'),
    (r'^actividades/crear/(\d+)/(\d+)/(\d+)$', 'ptrack.actividades.views.crear'),
    # arreglando para poder despachar js y css por media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^$', login, {'template_name': 'login.html'}),
    #(r'^logout/$', logout, {'template_name': 'logout.html'})
    (r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'})

)
