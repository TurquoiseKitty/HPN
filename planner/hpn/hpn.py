from typing import Callable, Dict, Generator, List, Optional, Set, Tuple
import logging

from planner.state import state_to_str
from planner.hpn.abstraction_level_dict import get_action_abstraction_level, increment_action_abstraction_level_and_duplicate_abstraction_dict
from planner.action import ActionSignature, Action
from planner.hpn.compute_predecessor_subgoal import ComputePredecessorSubgoal
from planner.hpn.generate_predecessor_subgoals import GenerateAllPredecessorSubgoals
from planner.backward_search import backward_search


# counts the number of fluents in goal
# that's not true in current state
# can be used as a simple heuristic function
def numFluentsNotSatisfied(goal: Set[Tuple], current_state: Set[Tuple]) -> int:
    return len(goal - current_state)


class HPN:

    def __init__(self, action_schemes: List[Action], check_consistency,
                 check_current_world_state_satisfy_goal) -> None:
        # domain-specific
        self.action_schemes = action_schemes
        self.check_consistency = check_consistency
        self.check_current_world_state_satisfy_goal = check_current_world_state_satisfy_goal

        self.compute_predecessor_subgoal = ComputePredecessorSubgoal()

    def __call__(
        self,
        current_world_state: Set[Tuple],
        goal: Set[Tuple],
        abstraction_level_dict: Dict[ActionSignature, int] = {},
        debug_func: Optional[Callable] = None
    ) -> Generator[Action, Set[Tuple], Set[Tuple]]:
        logging.debug(f"HPN CALLED with goal: \n{state_to_str(goal)}")
        generate_all_predecessor_subgoals = GenerateAllPredecessorSubgoals(
            computate_predecessor_subgoal=self.compute_predecessor_subgoal,
            check_consistency=self.check_consistency,
            abstraction_level_dict=abstraction_level_dict,
            actions=self.action_schemes)
        is_success, action_path, state_path = backward_search(
            current_world_state, goal, generate_all_predecessor_subgoals,
            numFluentsNotSatisfied, self.check_current_world_state_satisfy_goal)

        if not is_success:
            logging.warning("SEARCH FAILURE")
            return current_world_state

        if action_path is None or state_path is None:
            logging.info("Subgoal already satisfied, nothing to execute")
            return current_world_state

        # the first element is None, and a subgoal satisfied currently
        action_path.popleft()
        state_path.popleft()

        if debug_func is not None:
            debug_func(action_path, state_path, abstraction_level_dict)

        for action, subgoal in zip(action_path, state_path):
            abstract_level = get_action_abstraction_level(
                abstraction_level_dict, action)
            if action.is_primitive(abstract_level):
                current_world_state = yield action
            else:
                logging.debug(f"{action.action_signature} not primitive!")
                current_world_state = yield from self(
                    current_world_state, subgoal,
                    increment_action_abstraction_level_and_duplicate_abstraction_dict(
                        abstraction_level_dict, action), debug_func)

        return current_world_state
