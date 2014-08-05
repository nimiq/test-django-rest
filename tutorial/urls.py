from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include('snippets.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)