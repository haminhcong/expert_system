from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_property_list$', views.get_property_list, name='get_property_list'),
    url(r'^get_property_value',views.get_property_value,name='get_property_value'),
    url(r'^query_expert', views.query_expert, name='query_expert'),
    url(r'^rule_list', views.get_rule_list, name='rule_list'),
    url(r'^add_rule', views.add_rule, name='add_rule'),
    url(r'^edit_rule/(?P<rule_id>[0-9])', views.edit_rule, name='edit_rule'),
    url(r'^delete_rule_confirmation/(?P<rule_id>[0-9])', views.delete_rule_confirmation, name='delete_rule_confirmation'),
    url(r'^delete_rule', views.delete_rule, name='delete_rule')
]
