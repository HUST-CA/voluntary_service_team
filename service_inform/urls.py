from django.conf.urls import url

from . import views

app_name = 'service_inform'
urlpatterns = [
    url('^service/$', views.ServiceFormView.as_view(), name='service'),
    url('^service/(?P<tel>\d*?)/(?P<pk>\d*?)/$', views.OwnFlagView.as_view(), name='own_flag'),
    url('^(?P<short_link>.*?)/$', views.ShortLinkRedirect.as_view(), name='short_link_redirect'),
]
