from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /interviewMe/
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^interview/$', views.interview, name='interview'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^features/$', views.features, name='features'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^login/$', views.login, name='login'),
]
