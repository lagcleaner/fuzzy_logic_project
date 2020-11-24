
from fuzzy_system.membership_functions import *
from math import exp


class AbstractFuzzySet:
    '''
    Abstract class for a fuzzy set representation, only needs an `membership` method.
    '''

    def membership(self, x):
        raise NotImplementedError

# Custom FuzzySet


class CustomizableFuzzySet(AbstractFuzzySet):
    '''
    Generic fuzzy set with a domain and a membership function to be specified.
    '''

    def __init__(self, name: str, domain: tuple, membership_function=None):
        if membership_function is None:
            raise ValueError(
                'Membership function cant be None'
            )
        self.name = name
        self._membership = membership_function
        self.domain = domain

    def membership(self, x: float):
        return self._membership(x)

# Specific implementations


class GammaFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the gamma function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=13, b=17):
        if None in (name, a, b, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=self._gammamf
        )
        self.points = (a, b)

    def _gammamf(self, x):
        a, b = self.points

        if x <= a:
            return 0
        if a < x < b:
            return (x - a) / (b - a)
        if x >= b:
            return 1


class LambdaFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the lambda function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=13, b=17, middle=15):
        if None in (name, a, b, middle, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=self._lmbmf
        )
        self.points = (a, b, middle)

    def _lmbmf(self, x):
        a, b, middle = self.points

        if x <= a or x >= b:
            return 0
        if a < x <= middle:
            return (x - a) / (middle - a)
        if middle < x < b:
            return (b - x) / (b - middle)


class TrapezoidalFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the trapezoidal function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=12, b=14, c=16, d=18):
        if None in (name, a, b, c, d, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=self._trapmf
        )
        self.points = (a, b, c, d)

    def _trapmf(self, x):
        a, b, c, d = self.points

        if x <= a or x >= d:
            return 0
        if a < x < b:
            return (x - a) / (b - a)
        if b <= x <= c:
            return 1
        if c < x < d:
            return (d - x) / (d - c)


class SigmoidalFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the sigmoidal function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=12, b=18, middle=15):
        if None in (name, a, b, middle, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=self._smf
        )
        self.points = (a, b, middle)

    def _smf(self, x):
        a, b, middle = self.points

        middle = (a + b) / 2 if middle is None else middle
        if x <= a:
            return 0
        if a < x <= middle:
            return 2 * ((x - a) / (b - a)) ** 2
        if middle < x < b:
            return 1 - 2 * ((x - a) / (b - a)) ** 2
        if x >= b:
            return 1
        return 0


class GaussianFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the gaussian function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=3, middle=15):
        if None in (name, a, middle, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=self._gmf
        )
        self.points = (a,  middle)

    def _gmf(self, x):
        a, middle = self.points
        return exp(- a * (x - middle) ** 2)


# aliases
PiFuzzySet = TrapezoidalFuzzySet
TriangleFuzzySet = LambdaFuzzySet
