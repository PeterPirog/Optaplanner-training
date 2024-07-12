from optapy import solver_factory_create
from optapy.types import SolverConfig, Duration
from domain import KnapsackSolution, KnapsackItem, generate_problem
from constraints import define_constraints

def print_solution(solution: KnapsackSolution):
    print("Selected items:")
    for knapsack_item in solution.knapsack_item_list:
        if knapsack_item.in_knapsack:
            print(f"Item {knapsack_item.item.id}: weight={knapsack_item.item.weight}, value={knapsack_item.item.value}")

    total_weight = sum(item.item.weight for item in solution.knapsack_item_list if item.in_knapsack)
    total_value = sum(item.item.value for item in solution.knapsack_item_list if item.in_knapsack)
    print(f"Total weight: {total_weight}")
    print(f"Total value: {total_value}")

solver_config = SolverConfig().withEntityClasses(KnapsackItem) \
    .withSolutionClass(KnapsackSolution) \
    .withConstraintProviderClass(define_constraints) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))

solver = solver_factory_create(solver_config).buildSolver()

solution = solver.solve(generate_problem())

print_solution(solution)
