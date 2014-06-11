from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from playerinfo import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nomic.views.home', name='home'),
    # url(r'^nomic/', include('nomic.foo.urls')),

    url(r'^playerinfo/$', views.list_profiles, name=''),
    url(r'^playerinfo/login/$', views.login),
    url(r'^playerinfo/dashboard/$', views.dashboard),
    url(r'^playerinfo/dashboard/transfer/$', views.transfer),
    url(r'^playerinfo/dashboard/cancelbid/$', views.cancelbid),
    url(r'^playerinfo/dashboard/bid/$', views.bid),
    url(r'^playerinfo/dashboard/startup/$', views.startup),
    url(r'^playerinfo/dashboard/shutdown/$', views.shutdown),
    url(r'^playerinfo/dashboard/demolish/$', views.demolish),
    url(r'^playerinfo/dashboard/build/$', views.build),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
