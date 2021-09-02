from typing import Optional, Tuple, Set
from planner import action


class ComputePredecessorSubgoal:
    '''
    Regress one step:
    given a state of the world that we want to reach, 
    and an action that might help to reach that state,
    compute the state of the world before performing that action
    '''

    # def __init__(self, check_contradiction, check_entailment, conjoin) -> None:
    #     """passed in functions are part of domain description/knowledge"""
    #     self.check_contradiction = check_contradiction
    #     self.check_entailment = check_entailment
    #     self.conjoin = conjoin

    # def __call__(self, goal: Set[Tuple], action_instance: action.Action,
    #              fluent_regression_fn):
    #     '''
    #     compute predecessor subgoal
    #     implements the `regress` method in the HPN paper Appendix B.1
    #     '''
    #     subgoal = []
    #     for goal_fluent in goal:
    #         if self.check_contradiction(action_instance.add,
    #                                     goal_fluent,
    #                                     effect_negative=False):
    #             return False
    #         if self.check_contradiction(action_instance.delete,
    #                                     goal_fluent,
    #                                     effect_negative=True):
    #             return False
    #         if self.check_entailment(action_instance.add,
    #                                  goal_fluent,
    #                                  effect_negative=False):
    #             continue
    #         if self.check_entailment(action_instance.delete,
    #                                  goal_fluent,
    #                                  effect_negative=True):
    #             continue
    #         # TODO: fluent_regression_fn involves argument and chosen vars binding
    #         # should be part of action instance?
    #         subgoal = self.conjoin(subgoal, fluent_regression_fn(goal_fluent))
    #     for precondition_fluent in action_instance.precond:
    #         subgoal = self.conjoin(subgoal, precondition_fluent)
    #     return subgoal

    def __init__(self):
        pass

    def __call__(self, goal: Set[Tuple], preconditions: Set[Tuple],
                add_effects: Optional[Set[Tuple]]) -> Set[Tuple]:
        '''
        compute predecessor subgoal
        implements the `regress` method in the HPN paper Appendix B.1
        but using the simple set-theoretic approach for finite discrete domain
        '''

        predecessor_subgoal = goal - add_effects if add_effects is not None else goal
        predecessor_subgoal |= preconditions
        return predecessor_subgoal