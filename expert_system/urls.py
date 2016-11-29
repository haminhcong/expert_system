from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_property_list$', views.get_property_list, name='get_property_list'),
    url(r'^get_property_value',views.get_property_value,name='get_property_value'),
    url(r'^query_expert', views.query_expert, name='query_expert'),
]
