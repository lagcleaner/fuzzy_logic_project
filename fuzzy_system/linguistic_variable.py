
from fuzzy_system.fuzzy_set import AbstractFuzzySet
from fuzzy_system.fuzzy_proposition import MembershipProposition


class LinguisticVariable:
    def __init__(self, variable_name: str, *args):
        self.variable_name = variable_name
        if not all(isinstance(fset, AbstractFuzzySet) for fset in args):
            raise TypeError
        self.fuzzy_sets = {ufs.lv: ufs for ufs in args}

    def fuzzify(self, x, descriptor):
        return self.fuzzy_sets[descriptor].membership(x)

    def __eq__(self, other):
        if isinstance(other, str):
            return MembershipProposition(self, other)
        else:
            raise TypeError
