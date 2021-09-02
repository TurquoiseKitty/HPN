from typing import Callable, Generator, List, Tuple, Dict, Set

import planner.fluent

from planner.action import Action, bind_fluents_in_action, ActionSignature, get_considered_preconditions
from planner.hpn.abstraction_level_dict import get_action_abstraction_level


def generate_action_instances(action: Action,
                              previous_binding) -> List[Tuple[Action, Dict]]:
    """     
    operatorInstances function in HPN paper
    calls generator to generate multiple instances of the action
    """
    actions_instances = []
    if action.choose:
        variables_to_choose = action.choose
        generated_vals_for_choose = action.generator(previous_binding)
        for v in generated_vals_for_choose:
            choose_vars_binding_dict = dict(zip(variables_to_choose, v))
            payload = (bind_fluents_in_action(action,
                                              choose_vars_binding_dict), {
                                                  **choose_vars_binding_dict,
                                                  **previous_binding
                                              })
            actions_instances.append(payload)
    else:
        actions_instances.append((action, previous_binding))
    return actions_instances


def generate_relevant_action_and_binding(
        goal, actions) -> Generator[Tuple, None, None]:
    # action is relevant because it contributes to parts of the goal
    for goal_fluent in goal:
        for action in actions:
            for add_effect in action.add:
                unifiable, binding, _ = planner.fluent.unify(
                    add_effect, goal_fluent)
                if unifiable:
                    yield bind_fluents_in_action(action, binding), binding


class GenerateAllPredecessorSubgoals:
    '''
    given a state of the world that we would like to reach,
    consider all the possible actions that we might take just 
    before reaching that state, regress one steps on those actions,
    to generate all the possible predecessor states
    '''

    def __init__(self, abstraction_level_dict: Dict[ActionSignature, int],
                 computate_predecessor_subgoal,
                 check_consistency: Callable[[Set[Tuple]], bool],
                 actions: List[Action]) -> None:
        self.abstraction_level_dict = abstraction_level_dict
        self.computate_predecessor_subgoal = computate_predecessor_subgoal
        # check_consistency is part of domain description
        self.check_consistency = check_consistency
        self.actions = actions

    def __call__(self, goal: Set[Tuple]) -> List[Tuple[Action, Set[Tuple]]]:
        ''' ApplicableOps method in HPN paper (2012) Appendix B1, B2.
        '''

        # list of (operator_instance, subgoal)
        generated_subgoals = []

        for binded_action, binding in generate_relevant_action_and_binding(
                goal, self.actions):
            for action_instance, _ in generate_action_instances(
                    binded_action, binding):
                abstract_level = get_action_abstraction_level(
                    self.abstraction_level_dict, action_instance)
                preconditions = get_considered_preconditions(
                    abstract_level, action_instance)
                subgoal: Set[Tuple] = self.computate_predecessor_subgoal(
                    goal, preconditions, action_instance.add)
                # TODO: check consistency delete effect and subgoal
                if self.check_consistency(subgoal):

                    generated_subgoals.append((action_instance, subgoal))

        return generated_subgoals
