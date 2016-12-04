# from MarketingExpertSystem.model.rule import DatabaseRuleService
from expert_system.user.classify import classify_fact, get_list_left_fact


def backward_chaining(list_fact, list_rule):
    isResult = 0
    results = []
    list_fact_result = get_list_fact_result(list_fact)
    for fact in list_fact_result:
        how_list = []
        how_list = search_value(fact, how_list, list_fact, list_rule)
        if fact['value'] == '1':
            # results.append(fact)
            result = {
                'fact': fact,
                'how_list': how_list,
            }
            results.append(result)
            isResult = 1
    if isResult == 0:
        return 'result not found'
    return results


def get_list_fact_result(list_fact):
    list_fact_result = []
    for fact in list_fact:
        if fact['type'] == '3':
            list_fact_result.append(fact)
    return list_fact_result


def search_value(fact, how_list, list_fact, list_rule):
    for rule in list_rule:
        if fact['id'] == rule['right']:
            left_facts = get_list_left_fact(rule, list_fact)
            for left_fact in left_facts:
                if left_fact['type'] == '2':
                    search_value(left_fact, how_list)
            rule_value = calculor_value_fact(rule, left_facts)
            fact['value'] = rule_value
            fact['CF'] = calculor_value_CF(rule, left_facts)
            print fact['CF']
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
    while exp.find('~') > 0:
        index_not = exp.find('~')
        index_end = exp.find(')')
        str_not = exp[index_not + 1:index_end - 1]
        exp = exp.replace('(~' + str_not + ')', '-' + str_not)
    arr = []
    i = 0
    while i < len(exp):
        if exp[i] == '-':
            num = '-'
            j = i + 1
            while j < len(exp):
                if exp[j] != '|' and exp[j] != '^':
                    num += exp[j]
                    j += 1
                else:
                    break
            arr.append(float(num))
            i = j
        elif exp[i].isdigit():
            arr.append(int(exp[i]))
            i += 1
        else:
            arr.append(exp[i])
            i += 1
    while len(arr) > 1:
        try:
            index = arr.index('|')
            if index > 0:
                temp = max(arr[index - 1], arr[index + 1])
                arr = arr[:index - 1] + [temp] + arr[index + 2:]
        except Exception:
            arr = arr
        try:
            index = arr.index('^')
            if index > 0:
                temp = min(arr[index - 1], arr[index + 1])
                arr = arr[:index - 1] + [temp] + arr[index + 2:]
        except Exception:
            arr = arr
    return str(arr[0])
