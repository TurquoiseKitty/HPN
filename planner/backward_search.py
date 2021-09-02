from typing import Set, Tuple
from planner.astar import astar


# implementing the `PLAN` function in HPN paper Appendix B.1
def backward_search(current_world_state: Set[Tuple], subgoal: Set[Tuple],
                    generate_all_predecessor_subgoals,
                    heuristic_fn,
                    check_current_world_state_satisfy_goal):
    # we are using backwards search, so we start the search from the goal
    is_success, action_path, state_path = astar(
        starting_state=frozenset(subgoal),
        goal=current_world_state,
        generate_successors=generate_all_predecessor_subgoals,
        heuristic_func=heuristic_fn,
        goal_test=check_current_world_state_satisfy_goal)

    if is_success:
        if state_path is not None:
            state_path.reverse()
        if action_path is not None:
            action_path.reverse()
            action_path.rotate(1)
    return is_success, action_path, state_path
