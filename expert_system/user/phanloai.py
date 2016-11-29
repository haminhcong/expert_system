def phanloai(list_fact, list_rule):
    for fact in list_fact:
        left = False
        right = False
        for rule in list_rule:
            check_type = check(fact, rule, list_fact)
            if check_type == '2':
                left = True
                right = True
                break
            elif check_type == '1':
                left = True
            elif check_type == '3':
                right = True
        if left and right:
            fact['type'] = '2'
        elif left:
            fact['type'] = '1'
        elif right:
            fact['type'] = '3'
    return list_fact


def check(fact, rule, list_fact):
    fact_id = fact['id']
    list_fact = get_list_left_fact(rule, list_fact)
    list_fact_id = []
    for fact in list_fact:
        list_fact_id.append(fact['id'])
    if (fact_id in list_fact_id) and (fact_id == rule['right']):
        return '2'
    elif (fact_id in list_fact_id):
        return '1'
    elif fact_id == rule['right']:
        return '3'
    return '0'


def get_list_left_fact(rule, list_fact):
    left = rule['left']
    list_left_fact = []
    i = 0
    while i < len(left):
        if left[i].isdigit():
            j = i + 1
            fact = left[i]
            while j < len(left):
                if left[j].isdigit():
                    fact += left[j]
                    j += 1
                else:
                    break
            i = j
            for fac in list_fact:
                if fac['id'] == fact:
                    list_left_fact.append(fac)
                    break
        else:
            i += 1
    return list_left_fact
