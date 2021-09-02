from typing import Callable, List, NamedTuple, Optional, Set, Tuple
import functools
import json

import planner.fluent

FluentSet = Optional[Set[Tuple]]
ActionSignature = str


class Action(NamedTuple):
    name: str
    precond: List[FluentSet]
    add: FluentSet
    delete: FluentSet
    arguments: Optional[Tuple]
    choose: Optional[Tuple[str]]
    generator: Callable

    @property
    def action_signature(self) -> ActionSignature:
        # generate a representation of the action using action name and arguments

        if self.arguments is None:
            argument_encoding = ''
        else:
            argument_encoding = ', '.join(map(json.dumps, self.arguments))
        return "{}({})".format(self.name, argument_encoding)

    def is_primitive(self, abstract_level: int) -> bool:
        return abstract_level >= len(self.precond)-1


def bind_fluents_in_action(action: Action, binding) -> Action:
    """ground action"""
    new_argument = None
    if action.arguments is not None:
        new_argument = tuple(
            binding[arg] if arg in binding else arg for arg in action.arguments)
    new_precond = [
        planner.fluent.apply_binding_to_set_of_fluents(x, binding)
        for x in action.precond
    ]
    new_add = planner.fluent.apply_binding_to_set_of_fluents(
        action.add, binding)
    new_delete = planner.fluent.apply_binding_to_set_of_fluents(
        action.delete, binding)

    return Action(action.name, new_precond, new_add, new_delete, new_argument,
                  action.choose, action.generator)


def get_considered_preconditions(abstract_level: int,
                                 binded_action: Action) -> Set[Tuple]:
    # get the preconditions considered for current abstraction level

    consideredPreconditions: Set[Tuple] = functools.reduce(
        lambda accu, b: accu.union(b)
        if b else accu, binded_action.precond[:abstract_level+1], set())
    return consideredPreconditions