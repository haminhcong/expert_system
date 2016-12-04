from django.shortcuts import render
from django.http.response import HttpResponse
import json
from expert_system.user import classify,algorithm
from models import StoreItem, PropertyValue, ItemProperty, Fact


def index(request):
    item_list = StoreItem.objects.all()
    for item in item_list:
        item.image = str(item.id) + "_item.png"
    context = {'store_item_list': item_list}
    return render(request, 'expert_system/index.html', context)


def get_property_list(request):
    item_id = request.GET.get('id', None)
    item = StoreItem.objects.filter(id=item_id)
    property_list = item[0].itemproperty_set.all()
    property_data ={"property_list":[],'item_name':item[0].name}
    for property in property_list:
        first_value = property.propertyvalue_set.first()
        property_info = {"item_id":property.id,"name":property.property_name,
                         "first_value":{'id':first_value.id,'name':first_value.value}}
        property_data['property_list'].append(property_info)
    return HttpResponse(json.dumps(property_data), content_type='application/json')


def get_property_value(request):
    property_id = request.GET.get('id', None)
    property = ItemProperty.objects.filter(id=property_id)
    property_value_list = property[0].propertyvalue_set.all()
    property_data ={"value_list":[],'property_name':property[0].property_name,"property_id":property[0].id}
    for value_data in property_value_list:
        value_info = {'id':value_data.id,'value':value_data.value}
        property_data['value_list'].append(value_info)
    return HttpResponse(json.dumps(property_data), content_type='application/json')

def backward_charning(list_fact_input,list_rule):
    list_fact = Fact.objects.all()
    list_fact = classify.classify_fact(list_fact,list_rule)
    results = algorithm.backward_chaining(list_fact, list_rule)
    return results

def query_expert(request):
    if(request.method=="POST"):
        pass
    return HttpResponse(json.dumps({}), content_type='application/json')