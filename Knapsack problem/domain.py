import optapy
from optapy import problem_fact, planning_id, planning_entity, planning_variable, \
    planning_solution, planning_entity_collection_property, \
    problem_fact_collection_property, value_range_provider, planning_score
from optapy.types import HardSoftScore

@problem_fact
class Item:
    id: int
    weight: int
    value: int

    def __init__(self, id, weight, value):
        self.id = id
        self.weight = weight
        self.value = value

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"Item(id={self.id}, weight={self.weight}, value={self.value})"

@planning_entity
class KnapsackItem:
    id: int
    item: Item
    in_knapsack: bool

    def __init__(self, id, item, in_knapsack=False):
        self.id = id
        self.item = item
        self.in_knapsack = in_knapsack

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(bool, value_range_provider_refs=["booleanRange"])
    def get_in_knapsack(self):
        return self.in_knapsack

    def set_in_knapsack(self, in_knapsack):
        self.in_knapsack = in_knapsack

    def __str__(self):
        return f"KnapsackItem(id={self.id}, item={self.item}, in_knapsack={self.in_knapsack})"

@planning_solution
class KnapsackSolution:
    item_list: list[Item]
    knapsack_item_list: list[KnapsackItem]
    score: HardSoftScore

    def __init__(self, item_list, knapsack_item_list, score=None):
        self.item_list = item_list
        self.knapsack_item_list = knapsack_item_list
        self.score = score

    @problem_fact_collection_property(Item)
    @value_range_provider("itemRange")
    def get_item_list(self):
        return self.item_list

    @planning_entity_collection_property(KnapsackItem)
    def get_knapsack_item_list(self):
        return self.knapsack_item_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def __str__(self):
        return (
            f"KnapsackSolution("
            f"item_list={self.item_list},\n"
            f"knapsack_item_list={self.knapsack_item_list},\n"
            f"score={self.score}"
            f")"
        )

    @value_range_provider("booleanRange")
    def get_boolean_range(self):
        return [True, False]

def generate_problem():
    item_list = [
        Item(1, 4, 10),
        Item(2, 2, 4),
        Item(3, 2, 3),
        Item(4, 1, 2),
        Item(5, 5, 7)
    ]
    knapsack_item_list = [
        KnapsackItem(i, item) for i, item in enumerate(item_list, 1)
    ]
    return KnapsackSolution(item_list, knapsack_item_list)
