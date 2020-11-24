from fuzzy_system.linguistic_variable import LinguisticVariable
from fuzzy_system.norms import *


class FuzzyProposition:
    def __init__(self, tnorm=tnorm_min, tconorm=tconorm_max):
        self.tnorm = tnorm
        self.tconorm = tconorm

    def evaluate(self, values: dict):
        raise NotImplementedError()

    def __or__(self, other: FuzzyProposition):
        if isinstance(other, FuzzyProposition):
            return OrFuzzyProposition(self, other, tnorm=self.tnorm, tconorm=self.tconorm)
        else:
            raise TypeError

    def __and__(self, other: FuzzyProposition):
        if isinstance(other, FuzzyProposition):
            return AndFuzzyProposition(self, other, tnorm=self.tnorm, tconorm=self.tconorm)
        else:
            raise TypeError


class BinaryFuzzyProposition(FuzzyProposition):
    def __init__(self, proposition_l, proposition_r, tnorm=tnorm_min, tconorm=tconorm_max):
        self.proposition_l: BinaryFuzzyProposition = proposition_l
        self.proposition_r: BinaryFuzzyProposition = proposition_r


class AndFuzzyProposition(BinaryFuzzyProposition):
    def evaluate(self, values: dict):
        val_l = self.proposition_l.evaluate(values)
        val_r = self.proposition_r.evaluate(values)
        return self.tnorm(val_l, val_r)


class OrFuzzyProposition(BinaryFuzzyProposition):
    def evaluate(self, values: dict):
        val_l = self.proposition_l.evaluate(values)
        val_r = self.proposition_r.evaluate(values)
        return self.tconorm(val_l, val_r)


class NotFuzzyProposition(FuzzyProposition):
    def __init__(self, proposition: FuzzyProposition, tnorm=tnorm_min, tconorm=tconorm_max):
        super().__init__(tnorm=tnorm, tconorm=tconorm)
        self.proposition = proposition

    def evaluate(self, values: dict):
        val = self.proposition.evaluate(values)
        return 1 - val


class MembershipProposition(FuzzyProposition):
    def __init__(self, variable: LinguisticVariable, descriptor: str, tnorm=tnorm_min, tconorm=tconorm_max):
        super().__init__(tnorm=tnorm, tconorm=tconorm)
        self.variable = variable
        self.descriptor = descriptor

    def evaluate(self, values: dict):
        return self.variable.fuzzify(
            values[self.variable.variable_name], self.descriptor)
