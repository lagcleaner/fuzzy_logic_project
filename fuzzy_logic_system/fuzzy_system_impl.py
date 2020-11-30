from .fuzzy_set import UnionFuzzySet
from .dediffusion import centroid_dediffusion, bisection_dediffusion, mom_dediffusion, lom_dediffusion, som_dediffusion
from .norms import tconorm_max, tconorm_product


class FuzzyInferenceSystem:
    def __init__(self, rules: list):
        self.rules = rules

    def infer(self, values: dict, dediffusion_method=centroid_dediffusion, tconorm=tconorm_max):
        _, final_sets = self.rules[0].evaluate(values)
        for rule in self.rules[1:]:
            _, for_update = rule.evaluate(values)
            for var_name in for_update:
                final_sets[var_name] = UnionFuzzySet(
                    final_sets[var_name],
                    for_update[var_name],
                    tconorm=tconorm
                )

        return {
            var_name: dediffusion_method(cfs)
            for var_name, cfs in final_sets.items()
        }
