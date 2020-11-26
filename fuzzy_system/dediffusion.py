from numpy import arange
from fuzzy_system.fuzzy_set import CustomizableFuzzySet


def domain_sample(cfs: CustomizableFuzzySet, step=0.1):
    sample = list(arange(
        cfs.domain[0], cfs.domain[1], step)) + list(cfs.points)
    sample.sort()
    return sample


def centroid_dediffusion(cfs: CustomizableFuzzySet, step=0.1):
    '''
    Centroid
    '''
    data = domain_sample(cfs, step=step)
    sum_num = 0
    sum_den = 0
    for x in data:
        memb = cfs.membership(x)
        sum_num += x * memb
        sum_den += memb
    return sum_num / sum_den


def bisection_dediffusion(cfs: CustomizableFuzzySet, step=0.1):
    '''
    Bisection
    '''
    data = domain_sample(cfs, step=step)
    sums = [cfs.membership(data[0])]
    for x in data[1:]:
        sums.append(cfs.membership(x) + sums[-1])

    for i, x in enumerate(data):
        if sums[i] >= sums[-1] / 2:
            return x


def som_dediffusion(cfs: CustomizableFuzzySet, step=0.1):
    '''
    Smallest of Maximum
    '''
    data = domain_sample(cfs, step=step)
    return max(data, lambda x: cfs.membership(x))


def lom_dediffusion(cfs: CustomizableFuzzySet, step=0.1):
    '''
    Largest of Maximum
    '''

    data = domain_sample(cfs, step=step)
    data.reverse()
    return max(data, lambda x: cfs.membership(x))


def mom_dediffusion(cfs: CustomizableFuzzySet, step=0.1):
    '''
    Middle of Maximum
    '''
    min_max = som_dediffusion(cfs, step=step)
    max_max = lom_dediffusion(cfs, step=step)
    return (min_max + max_max)/2
