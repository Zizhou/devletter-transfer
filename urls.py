from django.conf.urls import patterns, url

from transfer import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
    #FUCKING regex
)
