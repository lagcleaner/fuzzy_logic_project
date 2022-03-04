import matplotlib.pyplot as plt
from fuzzy_logic_system import domain_sample, CustomizableFuzzySet


def graph(cfs: CustomizableFuzzySet):
    plt.xlabel('Domain values')
    plt.ylabel('Membership grade')
    plt.title(cfs.name)
    xs = domain_sample(cfs)
    ys = [cfs.membership(x) for x in xs]
    plt.plot(xs, ys)
    plt.show()
