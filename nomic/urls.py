from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from playerinfo import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nomic.views.home', name='home'),
    # url(r'^nomic/', include('nomic.foo.urls')),

    url(r'^playerinfo/$', views.list_profiles, name='pi-main'),
    url(r'^playerinfo/login/$', views.login, name='pi-login'),
    url(r'^playerinfo/dashboard/$', views.dashboard, name='pi-dashboard'),
    url(r'^playerinfo/dashboard/transfer/$', views.transfer, name='pi-transfer'),
    url(r'^playerinfo/dashboard/cancelbid/$', views.cancelbid, name='pi-cancelbid'),
    url(r'^playerinfo/dashboard/bid/$', views.bid, name='pi-bid'),
    url(r'^playerinfo/dashboard/startup/$', views.startup, name='pi-startup'),
    url(r'^playerinfo/dashboard/shutdown/$', views.shutdown, name='pi-shutdown'),
    url(r'^playerinfo/dashboard/demolish/$', views.demolish, name='pi-demolish'),
    url(r'^playerinfo/dashboard/build/$', views.build, name='pi-build'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
