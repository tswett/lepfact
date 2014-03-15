from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from playerinfo import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nomic.views.home', name='home'),
    # url(r'^nomic/', include('nomic.foo.urls')),

    url(r'^playerinfo/$', views.list_profiles, name=''),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
