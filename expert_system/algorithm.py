# from MarketingExpertSystem.model.rule import DatabaseRuleService

class BackWard:
    def __init__(self, list_fact, list_rule):
        self.list_fact = list_fact
        self.list_rule = list_rule

    def backward_chaining(self):
        isResult = 0
        results = []
        list_fact_result = self.get_list_fact_result()
        for fact in list_fact_result:
            how_list = []
            how_list = self.search_value(fact, how_list)
            if fact['value'] == '1':
                explation_list = []
                for rule in how_list:
                    lefts = []
                    for left_fact in rule['left']:
                        for fact_obj in self.list_fact:
                            if left_fact == fact_obj['id']:
                                lefts.append(fact_obj['content'])
                                break
                    right = None
                    for fact_obj in self.list_fact:
                        if rule['right'] == fact_obj['id']:
                            right = fact_obj['content']
                            break
                    explation_list.append({
                        'left':lefts,
                        'right':right,
                        'CF':rule['CF'],
                        'id':rule['id']
                    })
                result = {
                    'fact': fact,
                    'how_list': explation_list,
                }
                results.append(result)
                isResult = 1
        if isResult == 0:
            results = 'result not found'
        return results

    def get_list_fact_result(self):
        list_fact_result = []
        for fact in self.list_fact:
            if fact['type'] == '3':
                list_fact_result.append(fact)
        return list_fact_result

    def search_value(self, fact, how_list):
        for rule in self.list_rule:
            if fact['id'] == rule['right']:
                left_facts_id = rule['left']
                for left_fact in rule['left']:
                    fact_info = None
                    for fact_obj in self.list_fact:
                        if left_fact == fact_obj['id']:
                            fact_info = fact_obj
                            break
                    if fact_info['type'] == '2':
                        self.search_value(fact_info, how_list)
                rule_value = str(self.calculor_value_fact(left_facts_id))
                fact['value'] = rule_value
                fact['CF'] = self.calculor_value_CF(rule, left_facts_id)

                how_list.append(rule)
        return how_list

    def calculor_value_fact(self, left_facts_id):
        value = 1
        for fact_id in left_facts_id:
            fact_info = None
            for fact_obj in self.list_fact:
                if fact_id == fact_obj['id']:
                    fact_info = fact_obj
            value = int(fact_info['value']) and value
        return value

    def calculor_value_CF(self, rule, left_facts):
        value = 10000
        for fact_id in left_facts:
            fact_info = None
            for fact_obj in self.list_fact:
                if fact_id == fact_obj['id']:
                    fact_info = fact_obj
                    break
            value = min(fact_info['CF'], value)
        result = value * rule['CF']
        return result
