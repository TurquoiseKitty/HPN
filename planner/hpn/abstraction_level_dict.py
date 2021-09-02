from typing import Dict
import copy

from planner.action import Action, ActionSignature


def get_action_abstraction_level(abstraction_level_dict: Dict[ActionSignature,
                                                              int],
                                 action: Action):
    action_instance_signature = action.action_signature
    return abstraction_level_dict.get(action_instance_signature, 0)


# modifies abstraction_level_dict
def increment_action_abstraction_level(
        abstraction_level_dict: Dict[ActionSignature, int], action: Action):
    action_instance_signature = action.action_signature
    previous_abs_level = abstraction_level_dict.get(action_instance_signature,
                                                    0)
    abstraction_level_dict[action_instance_signature] = previous_abs_level + 1


def increment_action_abstraction_level_and_duplicate_abstraction_dict(
        abstraction_level_dict: Dict[ActionSignature, int], action: Action):
    new_abstraction_level_dict = copy.deepcopy(abstraction_level_dict)
    increment_action_abstraction_level(new_abstraction_level_dict, action)
    return new_abstraction_level_dict
