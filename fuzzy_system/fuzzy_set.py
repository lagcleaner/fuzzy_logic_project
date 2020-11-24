
from fuzzy_system.membership_functions import *


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
            membership_function=gammamf(a, b)
        )


class LambdaFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the lambda function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=13, b=17, m=15):
        if None in (name, a, b, m, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=lmbmf(a, b, m)
        )


class TrapezoidalFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the triangle function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=12, b=14, c=16, d=18):
        if None in (name, a, b, c, d, domain) or len(domain) != 2:
            raise ValueError
        super().__init__(
            name,
            domain,
            membership_function=trapmf(a, b, c, d)
        )


class SigmoidalFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the triangle function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (10, 20), a=12, b=18, middle=15):
        if None in (name, a, b, domain) or len(domain) != 2:
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
