from django.shortcuts import render
from django.http.response import HttpResponse
import json
from expert_system.user import classify, algorithm
from models import StoreItem, ItemProperty, Fact, RightFactModel, LeftFactModel, RuleModel
from django.shortcuts import redirect


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
    property_data = {"property_list": [], 'item_name': item[0].name}
    for property in property_list:
        first_value = property.propertyvalue_set.first()
        property_info = {"item_id": property.id, "name": property.property_name,
                         "first_value": {'id': first_value.id, 'name': first_value.value}}
        property_data['property_list'].append(property_info)
    return HttpResponse(json.dumps(property_data), content_type='application/json')


def get_property_value(request):
    property_id = request.GET.get('id', None)
    property = ItemProperty.objects.filter(id=property_id)
    property_value_list = property[0].propertyvalue_set.all()
    property_data = {"value_list": [], 'property_name': property[0].property_name, "property_id": property[0].id}
    for value_data in property_value_list:
        value_info = {'id': value_data.id, 'value': value_data.value}
        property_data['value_list'].append(value_info)
    return HttpResponse(json.dumps(property_data), content_type='application/json')


def backward_charning(list_fact_input, list_rule):
    list_fact = Fact.objects.all()
    list_fact = classify.classify_fact(list_fact, list_rule)
    results = algorithm.backward_chaining(list_fact, list_rule)
    return results


def query_expert(request):
    if request.method == "POST":
        pass
    return HttpResponse(json.dumps({}), content_type='application/json')


class RuleData:
    def __init__(self, rule_id, left_side, right_side, cf):
        self.rule_id = rule_id
        self.left_side = left_side
        self.right_side = right_side
        self.cf = cf


def get_rule_list(request):
    if request.method == "GET":
        rule_list = RuleModel.objects.all()
        rule_data = []
        for rule in rule_list:
            left_side = ''
            left_fact_list = rule.leftfactmodel_set.all()
            if len(left_fact_list) > 0:
                left_side = left_fact_list[0].content + '(' + left_fact_list[0].type + ')'
                for i in range(1, len(left_fact_list)):
                    left_side = left_side + ' and ' + left_fact_list[i].content + '(' + left_fact_list[i].type + ')'
            right_side = rule.right.content + '(' + str(rule.right.type) + ')'
            cf = rule.cf
            rule_id = rule.id
            rule_data.append(RuleData(rule_id, left_side, right_side, cf))
        context = {
            'rule_list': rule_data
        }
        return render(request, 'expert_system/rule_list.html', context)


def add_rule(request):
    if request.method == "GET":
        return render(request, 'expert_system/add_rule.html', {})

    if request.method == "POST":
        left_fact_list = []
        for x in range(1, 5):
            left_fact = request.POST['left-fact-' + str(x)]
            left_fact_type = request.POST['left-fact-' + str(x) + '-type']
            if len(left_fact) > 0:
                left_fact_list.append(LeftFactModel(content=left_fact, type=left_fact_type))
        right_fact_content = request.POST['right-fact']
        right_fact_type = request.POST['right-fact-type']

        right_fact = RightFactModel(content=right_fact_content, type=right_fact_type)
        right_fact.save()
        rule_cf = request.POST['rule-cf']
        new_rule = RuleModel(cf=rule_cf, right=right_fact)
        new_rule.save()

        for left_fact in left_fact_list:
            left_fact.rule_model = new_rule
            left_fact.save()
        return redirect(to='rule_list')


class ValueList:
    def __init__(self, id, value):
        self.id = id
        self.value = value


def edit_rule(request, rule_id):
    if request.method == "GET":
        rule = RuleModel.objects.filter(id=rule_id).first()
        new_left_fact_list = rule.leftfactmodel_set.all()
        right_fact = rule.right
        cf = rule.cf
        context = {}
        for x in range(0, len(new_left_fact_list)):
            context['left_fact_' + str(x + 1)] = new_left_fact_list[x].content
            context['left_fact_' + str(x + 1) + '_type'] = int(new_left_fact_list[x].type)
            # context['left_fact_' + str(x + 1) + '_type'] = 2

        for x in range(len(new_left_fact_list), 5):
            context['left_fact_' + str(x + 1)] = ''
            context['left_fact_' + str(x + 1) + '_type'] = 1
        right_fact.type = int(right_fact.type)
        context['right_fact'] = right_fact
        context['cf'] = cf
        context['rule_id'] = rule.id
        context['value_list'] = [ValueList(1, 'Start fact'), ValueList(2, 'Middle Fact'), ValueList(3, 'End Fact')]
        return render(request, 'expert_system/edit_rule.html', context)

    if request.method == "POST":
        rule_id = request.POST['rule_id']
        current_rule = RuleModel.objects.filter(id=rule_id).first()
        old_left_fact_list = current_rule.leftfactmodel_set.all()
        for old_fact  in old_left_fact_list:
            old_fact.delete()
        new_left_fact_list = []
        for x in range(1, 5):
            left_fact = request.POST['left-fact-' + str(x)]
            left_fact_type = request.POST['left-fact-' + str(x) + '-type']
            if len(left_fact) > 0:
                new_left_fact_list.append(LeftFactModel(content=left_fact, type=left_fact_type))
        new_right_fact_content = request.POST['right-fact']
        right_fact_type = request.POST['right-fact-type']
        current_right_fact =  current_rule.right
        rule_cf = request.POST['rule-cf']
        current_right_fact.content = new_right_fact_content
        current_right_fact.type =right_fact_type
        current_rule.cf = rule_cf
        current_right_fact.save()
        current_rule.save()
        for new_left_fact in new_left_fact_list:
            new_left_fact.rule_model = current_rule
            new_left_fact.save()
        return redirect(to='rule_list')


def delete_rule_confirmation(request, rule_id):
    if request.method == "GET":
        rule = RuleModel.objects.filter(id=rule_id).first()
        left_fact_list = rule.leftfactmodel_set.all()
        left_side = ''
        if len(left_fact_list) > 0:
            left_side = left_fact_list[0].content + '(' + left_fact_list[0].type + ')'
            for i in range(1, len(left_fact_list)):
                left_side = left_side + ' and ' + left_fact_list[i].content + '(' + left_fact_list[i].type + ')'
        right_side = rule.right.content + '(' + str(rule.right.type) + ')'
        cf = rule.cf

        rule_mean = left_side + ' => ' + right_side + ' : CF=' + str(cf)
        context = {'rule_id': rule_id, 'rule_mean': rule_mean}
        return render(request, 'expert_system/delete_rule.html', context)


def delete_rule(request):
    if request.method == "POST":
        rule_id = request.POST['rule_id']
        deleted_rule = RuleModel.objects.filter(id=rule_id).first()
        deleted_rule.right.delete()
        deleted_rule.delete()
        return redirect(to='rule_list')
