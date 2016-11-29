# from MarketingExpertSystem.model.rule import DatabaseRuleService
from expert_system.user.phanloai import phanloai, get_list_left_fact

list_fact = [{
    'id': '1',
    'type': '0',
    'mean': 'su kien 1',
    'value': '1',
    'isValue': '1',
    'CF': '3',
}, {
    'id': '2',
    'type': '0',
    'mean': 'su kien 2',
    'value': '1',
    'isValue': '1',
    'CF': '1',
}, {
    'id': '3',
    'type': '0',
    'mean': 'su kien 3',
    'value': '1',
    'isValue': '1',
    'CF': '2',
}, {
    'id': '4',
    'type': '0',
    'mean': 'su kien 4',
    'value': '0',
    'isValue': '0',
    'CF': '4',
}, {
    'id': '5',
    'type': '0',
    'mean': 'su kien 5',
    'value': '0',
    'isValue': '0',
    'CF': '',
}, {
    'id': '6',
    'type': '0',
    'mean': 'su kien 6',
    'value': '0',
    'isValue': '0',
    'CF': '',
}, {
    'id': '7',
    'type': '0',
    'mean': 'su kien 7',
    'value': '0',
    'isValue': '0',
    'CF': '',
}, {
    'id': '8',
    'type': '0',
    'mean': 'su kien 8',
    'value': '0',
    'isValue': '0',
    'CF': '',
}, {
    'id': '9',
    'type': '0',
    'mean': 'su kien 9',
    'value': '0',
    'isValue': '0',
    'CF': '',
}]

list_rule = [{
    'id': '1',
    'left': '1 AND 2',
    'right': '5',
}, {
    'id': '2',
    'left': '3',
    'right': '6',
}, {
    'id': '3',
    'left': '3 OR 4',
    'right': '7',
}, {
    'id': '4',
    'left': '5 AND 6',
    'right': '8',
},{
    'id':'5',
    'left':'7',
    'right':'9',
}]

phanloai(list_fact, list_rule)


def forward_chaining():
    isResult = 0
    results = []
    list_fact_result = get_list_fact_result()
    for fact in list_fact_result:
        how_list = []
        how_list = search_value(fact, how_list)
        if fact['value'] == '1':
            results.append(fact)
            print ('how list: ', how_list)
            print(fact)
            isResult = 1
    if isResult == 0:
        return 'result not found'
    return results


def get_list_fact_result():
    list_fact_result = []
    for fact in list_fact:
        if fact['type'] == '3':
            list_fact_result.append(fact)
    return list_fact_result


def search_value(fact, how_list):
    for rule in list_rule:
        if fact['id'] == rule['right']:
            left_facts = get_list_left_fact(rule, list_fact)
            for left_fact in left_facts:
                if left_fact['type'] == '2':
                    search_value(left_fact, how_list)
            rule_value = calculor_value_fact(rule, left_facts)
            fact['value'] = rule_value
            how_list.append(rule)
    return how_list


def calculor_value_fact(rule, left_facts):
    exp = rule['left']
    exp = exp.replace(' ', '')
    exp = exp.replace('NOT', '~')
    exp = exp.replace('AND', '^')
    exp = exp.replace('OR', '|')
    for fact in left_facts:
        exp = exp.replace(fact['id'], fact['value'])
    exp = exp.replace('(~1)', '0')
    exp = exp.replace('(~0)', '1')
    while len(exp) > 1:
        index = exp.find('^')
        if index != -1:
            temp = int(exp[index - 1]) & int(exp[index + 1])
            exp = exp.replace(exp[index - 1] + '^' + exp[index + 1], str(temp))
        index1 = exp.find('|')
        if index1 != -1:
            temp1 = int(exp[index1 - 1]) | int(exp[index1 + 1])
            exp = exp.replace(exp[index1 - 1] + '|' + exp[index1 + 1], str(temp1))
    return exp

def calculor_value_CF(rule, left_facts):
    exp = rule['left']
    exp = exp.replace(' ', '')
    exp = exp.replace('NOT', '~')
    exp = exp.replace('AND', '^')
    exp = exp.replace('OR', '|')
    for fact in left_facts:
        exp = exp.replace(fact['id'], fact['CF'])
    # index_not = exp.find('x')
    while exp.find('~') > 0:
        index_not = exp.find('~')
        index_end = exp.find(')')
        str_not = exp[index_not+1:index_end-1]
        exp = exp.replace('(~'+str_not+')','-'+str_not)
        print (str_not)

    while len(exp) > 2:
        index = exp.find('^')
        if index != -1:
            temp = int(exp[index - 1]) & int(exp[index + 1])
            exp = exp.replace(exp[index - 1] + '^' + exp[index + 1], str(temp))
        index1 = exp.find('|')
        if index1 != -1:
            temp1 = int(exp[index1 - 1]) | int(exp[index1 + 1])
            exp = exp.replace(exp[index1 - 1] + '|' + exp[index1 + 1], str(temp1))
    return exp

result = forward_chaining()
