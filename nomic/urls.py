from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from playerinfo import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nomic.views.home', name='home'),
    # url(r'^nomic/', include('nomic.foo.urls')),

    url(r'^playerinfo/$', views.list_profiles, name=''),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
