from fuzzy_system.fuzzy_proposition import FuzzyProposition
from fuzzy_system.fuzzy_set import FuzzySet, MamdaniCut, LarsenScale

# FuzzyConsequent = type(tuple(_, _))


class FuzzyRule:
    '''
    A General Rule for apply any method of inference.
    '''

    def __init__(self, proposition: FuzzyProposition, consequent: list, method_transformer=None):
        self.transformer = method_transformer
        self.proposition = proposition
        self.consequent = consequent

    def evaluate(self, values: dict):
        prepos_value: float = self.proposition.evaluate(values)
        conseq_transformed_sets = {}
        if not (self.transformer is None):
            for variable, descrip in self.consequent:
                fs = variable.descriptors[descrip]
                conseq_transformed_sets[variable.name] = \
                    self.transformer(
                    prepos_value,
                    fs
                )
        return prepos_value, conseq_transformed_sets


class MamdaniRule(FuzzyRule):
    def __init__(self, preposition: FuzzyProposition, consequent: list):
        super().__init__(
            preposition,
            consequent,
            method_transformer=lambda val, fs: MamdaniCut(fs, val)
        )


class LarsenRule(FuzzyRule):
    def __init__(self, preposition: FuzzyProposition, consequent: list):
        super().__init__(
            preposition,
            consequent,
            method_transformer=lambda val, fs: LarsenScale(fs, val)
        )
