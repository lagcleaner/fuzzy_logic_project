from .fuzzy_set import FuzzySet
from .norms import tconorm_max, tconorm_product, tnorm_min, tnorm_product

# region Language Variable


class LanguageVariable:
    def __init__(self, name: str, *args):
        self.name = name
        if not all(isinstance(fset, FuzzySet) for fset in args):
            raise TypeError
        self.fuzzy_sets = {ufs.name: ufs for ufs in args}

    def fuzzify(self, x, descriptor):
        return self.fuzzy_sets[descriptor].membership(x)

    def __mod__(self, other):
        if isinstance(other, str):
            return MembershipProposition(self, other)
        else:
            raise TypeError


# endregion

# region Fuzzy Proposition

class FuzzyProposition:
    def __init__(self, tnorm=tnorm_min, tconorm=tconorm_max):
        self.tnorm = tnorm
        self.tconorm = tconorm

    def evaluate(self, values: dict):
        raise NotImplementedError()

    def __or__(self, other):
        if isinstance(other, FuzzyProposition):
            return OrFuzzyProposition(self, other, tnorm=self.tnorm, tconorm=self.tconorm)
        else:
            raise TypeError

    def __and__(self, other):
        if isinstance(other, FuzzyProposition):
            return AndFuzzyProposition(self, other, tnorm=self.tnorm, tconorm=self.tconorm)
        else:
            raise TypeError

    def __invert__(self):
        return NotFuzzyProposition(self, tnorm=self.tnorm, tconorm=self.tconorm)


# region Binary Operations
class BinaryFuzzyProposition(FuzzyProposition):
    def __init__(self, proposition_l, proposition_r, tnorm=tnorm_min, tconorm=tconorm_max):
        super().__init__(tnorm=tnorm, tconorm=tconorm)
        self.proposition_l: FuzzyProposition = proposition_l
        self.proposition_r: FuzzyProposition = proposition_r


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

# endregion


# region Unary Operations
class NotFuzzyProposition(FuzzyProposition):
    def __init__(self, proposition: FuzzyProposition, tnorm=tnorm_min, tconorm=tconorm_max):
        super().__init__(tnorm=tnorm, tconorm=tconorm)
        self.proposition = proposition

    def evaluate(self, values: dict):
        val = self.proposition.evaluate(values)
        return 1 - val


class MembershipProposition(FuzzyProposition):
    def __init__(self, variable: LanguageVariable, descriptor: str, tnorm=tnorm_min, tconorm=tconorm_max):
        super().__init__(tnorm=tnorm, tconorm=tconorm)
        self.variable = variable
        self.descriptor = descriptor

    def evaluate(self, values: dict):
        return self.variable.fuzzify(
            values[self.variable.name], self.descriptor)

# endregion

# endregion
