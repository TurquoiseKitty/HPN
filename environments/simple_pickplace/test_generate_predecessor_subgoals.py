# %%
from IPython import get_ipython

ipython = get_ipython()
if ipython is not None:
    ipython.magic("load_ext autoreload")
    ipython.magic("autoreload 2")

# %%
from typing import Set, Tuple

from planner.hpn.generate_predecessor_subgoals import GenerateAllPredecessorSubgoals
from planner.hpn.compute_predecessor_subgoal import ComputePredecessorSubgoal
from planner.state import state_to_str

from environments.simple_pickplace.domain import PREDICATES, check_consistency, WASH_GRID
from environments.simple_pickplace.action_schemes import ACTION_SCHEMES

# define the problem
goal: Set[Tuple] = set()
# goal.add((PREDICATES.COOKED, "a"))
# goal.add((PREDICATES.OBJ_LOC, "a", WASH_GRID))
# goal.add((PREDICATES.GRID_CLEAR, 0))
goal.add((PREDICATES.IN, "a", (0, 0)))
state_to_str(goal)

# %%
# test
compute_predecessor_subgoal = ComputePredecessorSubgoal()
generate_all_predecessor_subgoals = GenerateAllPredecessorSubgoals(
    {}, compute_predecessor_subgoal, check_consistency, ACTION_SCHEMES)
predecessors = generate_all_predecessor_subgoals(goal)

for a, s in predecessors:
    print(a.action_signature)
    state_to_str(s)
# %%
