

def gammamf(a, b):
    '''
            __
        __/
    '''
    def _gammamf(x):
        if x <= a:
            return 0
        if a < x < b:
            return (x - a) / (b - a)
        if x >= b:
            return 1
    return _gammamf


def lmf(a, m):
    def _lmf(x):
        if x <= a:
            return 1
        if a < x < m:
            return (m - x) / (m - a)
        if x >= m:
            return 0
    return _lmf


def lmbmf(a, b, m):
    '''
    _/\\\\_
    '''
    def _lmbmf(x):
        if x <= a or x >= b:
            return 0
        if a < x <= m:
            return (x - a) / (m - a)
        if m < x < b:
            return (b - x) / (b - m)
    return _lmbmf


def trapmf(a, b, c, d):
    def _trapmf(x):
        if x <= a or x >= d:
            return 0
        if a < x < b:
            return (x - a) / (b - a)
        if b <= x <= c:
            return 1
        if c < x < d:
            return (d - x) / (d - c)
    return _trapmf


def gaussmf(m, a):
    _smf = smf(m - a, m)
    _zmf = zmf(m, m + a)

    def _gaussmf(x):
        if x <= m:
            return _smf(x)
        if x > m:
            return _smf(x)
    return _gaussmf


def smf(a, b, middle=None):
    def _smf(x):
        middle = (a + b) / 2 if middle is None else middle
        if x <= a:
            return 0
        if a < x <= middle:
            return 2 * ((x - a) / (b - a)) ** 2
        if middle < x < b:
            return 1 - 2 * ((x - a) / (b - a)) ** 2
        if x >= b:
            return 1
    return _smf


def zmf(a, c):
    '''
    1 - smf
    '''
    def _zmf(x):
        middle = (a + c) / 2
        if x <= a:
            return 1
        if a < x <= middle:
            return 1 - 2 * ((x - a) / (c - a)) ** 2
        if middle < x < c:
            return 2 * ((x - a) / (c - a)) ** 2
        if x >= c:
            return 0
    return _zmf
