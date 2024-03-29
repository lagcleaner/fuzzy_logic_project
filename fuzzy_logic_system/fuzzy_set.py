
from math import exp
from .norms import tconorm_max, tconorm_product, tnorm_min, tnorm_product


class FuzzySet:
    '''
    Abstract class for a fuzzy set representation, only needs an `membership` method.
    '''

    def __init__(self, name: str):
        self.name = name

    def membership(self, x):
        raise NotImplementedError


# region Custom FuzzySet


class CustomizableFuzzySet(FuzzySet):
    '''
    Generic fuzzy set with a domain and a membership function to be specified on parameters.
    '''

    def __init__(self, name: str, domain: tuple, membership_function=None, points=[]):
        super().__init__(name)
        if membership_function is None:
            raise ValueError(
                'Membership function cant be None'
            )
        self.name = name
        self._membership = membership_function
        self.domain = domain
        self.points = points

    def __add__(self, other):
        if not isinstance(other, FuzzySet):
            raise TypeError
        return UnionFuzzySet(self, other)

    def membership(self, x: float):
        return self._membership(x)

# endregion

# region Specific implementations


class GammaFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the gamma function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> (a, b)
        if points == None or len(points) != 2:
            points = (domain[0], domain[1])
        super().__init__(
            name,
            domain,
            membership_function=self._gammamf,
            points=points
        )

    def _gammamf(self, x):
        a, b = self.points

        if x <= a:
            return 0
        if a < x < b:
            return (x - a) / (b - a)
        if x >= b:
            return 1


class LFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the L function as membership function.(opposite of gamma)
    '''

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> (a, b)
        if points == None or len(points) != 2:
            points = (domain[0], domain[1])
        super().__init__(
            name,
            domain,
            membership_function=self._lmf,
            points=points
        )

    def _lmf(self, x):
        a, b = self.points

        if x <= a:
            return 1
        if a < x < b:
            return (b - x) / (b - a)
        if x >= b:
            return 0


class LambdaFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the lambda function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> a, b, middle
        if points == None or len(points) != 3:
            points = domain[0], domain[1], (domain[0] + domain[1]) / 2
        super().__init__(
            name,
            domain,
            membership_function=self._lmbmf,
            points=points
        )

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

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> (a, b, c, d)
        if points == None or len(points) != 4:
            points = (
                domain[0],
                (domain[0] + domain[1]) / 3,
                2 * (domain[0] + domain[1]) / 3,
                domain[1]
            )
        super().__init__(
            name,
            domain,
            membership_function=self._trapmf,
            points=points
        )

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

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> (a, b, middle)
        if points == None or len(points) != 3:
            points = (
                domain[0],
                domain[1],
                (domain[0] + domain[1]) / 2,
            )
        super().__init__(
            name,
            domain,
            membership_function=self._smf,
            points=points
        )

    def _smf(self, x):
        a, b, middle = self.points

        middle = (a + b) / 2 if middle is None else middle
        if x <= a:
            return 0
        if a < x <= middle:
            return 2 * ((x - a) / (b - a)) ** 2
        if middle < x < b:
            return 1 - 2 * ((b - x) / (b - a)) ** 2
        if x >= b:
            return 1


class ZFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the Z function as membership function.(opposite of sigmoidal)
    '''

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> (a, b, middle)
        if points == None or len(points) != 3:
            points = (
                domain[0],
                domain[1],
                (domain[0] + domain[1]) / 2,
            )
        super().__init__(
            name,
            domain,
            membership_function=self._smf,
            points=points
        )

    def _smf(self, x):
        a, b, middle = self.points

        middle = (a + b) / 2 if middle is None else middle
        if x <= a:
            return 1
        if a < x <= middle:
            return 1 - 2 * ((x - a) / (b - a)) ** 2
        if middle < x < b:
            return 2 * ((b - x) / (b - a)) ** 2
        if x >= b:
            return 0


class GaussianFuzzySet(CustomizableFuzzySet):
    '''
    Fuzzy Set whit the gaussian function as membership function.
    '''

    def __init__(self, name: str, domain: tuple = (0, 20), points=None):
        # points -> (a, middle)
        if points == None or len(points) != 2:
            points = (
                domain[0],
                domain[1],
                (domain[0] + domain[1]) / 2,
            )
        super().__init__(
            name,
            domain,
            membership_function=self._gmf,
            points=points
        )

    def _gmf(self, x):
        a, b, middle = self.points

        if x <= a:
            return 0
        if a < x <= middle:  # s function
            return 2 * ((x - a) / (b - a)) ** 2
        if middle < x < b:  # z function
            return 2 * ((b - x) / (b - a)) ** 2
        if x >= b:
            return 0

# endregion

# region Composed Fuzzy Set


class UnionFuzzySet(CustomizableFuzzySet):
    def __init__(self, fuzzy_set1: CustomizableFuzzySet, fuzzy_set2: CustomizableFuzzySet, tconorm=tconorm_max):
        self.tconorm = tconorm
        self.fs1 = fuzzy_set1
        self.fs2 = fuzzy_set2
        super().__init__(
            '_U_'.join((fuzzy_set1.name, fuzzy_set2.name)),
            (
                min(fuzzy_set1.domain[0], fuzzy_set2.domain[0]),
                max(fuzzy_set1.domain[1], fuzzy_set2.domain[1])
            ),
            membership_function=self._union,
            points=fuzzy_set1.points + fuzzy_set2.points
        )

    def _union(self, x):
        return self.tconorm(
            self.fs1.membership(x),
            self.fs2.membership(x)
        )


# endregion

# region Mamdani and Larsen Fuzzy Set modifiers


class MamdaniCut(CustomizableFuzzySet):
    def __init__(self, fuzzy_set: CustomizableFuzzySet, value: float):
        self.value = value
        self.origin = fuzzy_set
        super().__init__(
            'mamdani_{}'.format(fuzzy_set.name),
            domain=fuzzy_set.domain,
            membership_function=self._mamdani,
            points=fuzzy_set.points
        )

    def _mamdani(self, x):
        return min(self.value, self.origin.membership(x))


class LarsenScale(CustomizableFuzzySet):
    def __init__(self, fuzzy_set: CustomizableFuzzySet, value: float):
        self.value = value
        self.origin = fuzzy_set
        super().__init__(
            'larsen_{}'.format(fuzzy_set.name),
            domain=fuzzy_set.domain,
            membership_function=self._larsen,
            points=fuzzy_set.points
        )

    def _larsen(self, x):
        return (self.value * self.origin.membership(x))

# endregion


# region Aliases
PiFuzzySet = TrapezoidalFuzzySet
TriangleFuzzySet = LambdaFuzzySet

# endregion
