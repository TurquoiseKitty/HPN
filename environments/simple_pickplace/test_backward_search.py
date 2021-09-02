# %%
from IPython import get_ipython

ipython = get_ipython()
if ipython is not None:
    ipython.magic("load_ext autoreload")
    ipython.magic("autoreload 2")

# %%
from typing import Set, Tuple

from planner.state import state_to_str

from environments.simple_pickplace.domain import PREDICATES, check_consistency, goal_test, WASH_GRID
from environments.simple_pickplace.action_schemes import ACTION_SCHEMES

# define the problem
current_state: Set[Tuple] = set()
current_state.add((PREDICATES.OBJ_LOC, "a", 3))
current_state.add((PREDICATES.OBJ_LOC, "b", 1))
state_to_str(current_state)

goal: Set[Tuple] = set()
# goal.add((PREDICATES.OBJ_LOC, "a", WASH_GRID))
# goal.add((PREDICATES.CLEAN, "a"))
goal.add((PREDICATES.OBJ_LOC, "a", 1))
# goal.add((PREDICATES.COOKED, "a"))

state_to_str(goal)

# %%
from planner.backward_search import backward_search
from planner.hpn.generate_predecessor_subgoals import GenerateAllPredecessorSubgoals
from planner.hpn.compute_predecessor_subgoal import ComputePredecessorSubgoal
from planner.hpn.hpn import numFluentsNotSatisfied

generate_all_predecessor_subgoals = GenerateAllPredecessorSubgoals(
    computate_predecessor_subgoal=ComputePredecessorSubgoal(),
    check_consistency=check_consistency,
    abstraction_level_dict={},
    actions=ACTION_SCHEMES)
is_success, action_path, state_path = backward_search(
    current_state, goal, generate_all_predecessor_subgoals,
    numFluentsNotSatisfied, goal_test)

# %%

for a, s in zip(action_path, state_path):
    if a is not None:
        print(a.action_signature)
    else:
        print(a)
    state_to_str(s)
# %%
