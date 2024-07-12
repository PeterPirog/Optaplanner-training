from optapy import constraint_provider
from optapy.score import HardSoftScore
from optapy.constraint import ConstraintFactory
from domain import KnapsackItem

MAX_WEIGHT = 10

@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        max_weight_constraint(constraint_factory),
        maximize_value(constraint_factory)
    ]

def max_weight_constraint(constraint_factory: ConstraintFactory):
    # The total weight of items in the knapsack must not exceed MAX_WEIGHT.
    return constraint_factory \
        .for_each(KnapsackItem) \
        .filter(lambda knapsack_item: knapsack_item.in_knapsack) \
        .group_by(lambda knapsack_item: sum(knapsack_item.item.weight)) \
        .filter(lambda total_weight: total_weight > MAX_WEIGHT) \
        .penalize("Max weight constraint", HardSoftScore.ONE_HARD)

def maximize_value(constraint_factory: ConstraintFactory):
    # Maximize the total value of items in the knapsack.
    return constraint_factory \
        .for_each(KnapsackItem) \
        .filter(lambda knapsack_item: knapsack_item.in_knapsack) \
        .group_by(lambda knapsack_item: sum(knapsack_item.item.value)) \
        .reward("Maximize value", HardSoftScore.ONE_SOFT)
