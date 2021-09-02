# %%
from IPython import get_ipython

ipython = get_ipython()
if ipython is not None:
    ipython.magic("load_ext autoreload")
    ipython.magic("autoreload 2")

# %%
from typing import Set, Tuple

from planner.state import state_to_str
from planner.hpn.hpn import HPN

from environments.simple_pickplace.domain import PREDICATES, check_consistency, goal_test
from environments.simple_pickplace.action_schemes import ACTION_SCHEMES

# define the problem
current_state: Set[Tuple] = set()
current_state.add((PREDICATES.OBJ_LOC, "a", 0))
current_state.add((PREDICATES.OBJ_LOC, "b", 1))
print(state_to_str(current_state))

goal: Set[Tuple] = set()
goal.add((PREDICATES.COOKED, "a"))
print(state_to_str(goal))

# %%
hpn = HPN(ACTION_SCHEMES,
          check_consistency=check_consistency,
          check_current_world_state_satisfy_goal=goal_test)
plan = hpn(current_state, goal)

for a in plan:
    if a is not None:
        print(a.action_signature)
    else:
        print(a)

# %%
