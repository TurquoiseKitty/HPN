# %%
from typing import List, Set, Tuple

from traitlets.traitlets import All

from planner.action import Action
from environments.simple_pickplace.domain import PREDICATES, WASH_GRID, COOK_GRID, ALL_GRIDS, ALL_OBJECTS


# %%
def def_wash_action():
    ARGS = ("$food",)

    precond_0 = None
    precond_1 = set([(PREDICATES.OBJ_LOC, ARGS[0], WASH_GRID)])
    return Action(name="Wash",
                  precond=[precond_0, precond_1],
                  add=set([(PREDICATES.CLEAN, ARGS[0])]),
                  delete=set(),
                  arguments=ARGS,
                  choose=None,
                  generator=None)


def def_cook_action():
    ARGS = ("$food",)
    precond_0 = None
    precond_1 = set([(PREDICATES.CLEAN, ARGS[0])])
    precond_2 = set([(PREDICATES.OBJ_LOC, ARGS[0], COOK_GRID)])
    return Action(name="Cook",
                  precond=[precond_0, precond_1, precond_2],
                  add=set([(PREDICATES.COOKED, ARGS[0])]),
                  delete=set([]),
                  arguments=ARGS,
                  choose=None,
                  generator=None)


def def_pick_place_action():
    ARG_FOOD = "$food"
    ARG_DEST = "$dest"
    CHOOSE_START = "$start"

    effect_add: Set[Tuple] = set()
    effect_add.add((PREDICATES.OBJ_LOC, ARG_FOOD, ARG_DEST))

    effect_delete: Set[Tuple] = set()
    effect_delete.add((PREDICATES.OBJ_LOC, ARG_FOOD, CHOOSE_START))
    effect_delete.add((PREDICATES.REGION_CLEAR, (CHOOSE_START, ARG_DEST)))

    precond_0: Set[Tuple] = set()
    precond_0.add((PREDICATES.OBJ_LOC, ARG_FOOD, CHOOSE_START))
    precond_0.add((PREDICATES.REGION_CLEAR, (CHOOSE_START, ARG_DEST)))

    # precond_0.add((PREDICATES.GRID_CLEAR, ARG_DEST))

    def _gen(binding):
        dest = binding[ARG_DEST]
        for i in ALL_GRIDS:
            if i != dest:
                yield (i,)

    return Action(name="PickPlace",
                  precond=[precond_0],
                  add=effect_add,
                  delete=effect_delete,
                  arguments=(ARG_FOOD, ARG_DEST),
                  choose=(CHOOSE_START,),
                  generator=_gen)


# region will be in the form (START, END)
# END is included in the region
# START is not included in the region
def region_to_range(REGION):

    if len(REGION) == 1:
        return (REGION[0], REGION[0] + 1)
    else:
        start, end = REGION
        # start is not included, end is
        if start < end:
            position_min = start + 1
            position_max = end + 1
        else:
            position_min = end
            position_max = start
        return (position_min, position_max)


def def_clear_region_definitional_action():
    ARG_REGION = "$region"
    precond_0 = set()
    for obj in ALL_OBJECTS:
        precond_0.add((PREDICATES.IN, obj, 0, ARG_REGION))
    effect_add = set()
    effect_add.add((PREDICATES.REGION_CLEAR, ARG_REGION))
    effect_delete = precond_0
    return Action(name="Clear_Region",
                  precond=[
                      precond_0,
                  ],
                  add=effect_add,
                  delete=effect_delete,
                  arguments=(ARG_REGION,),
                  choose=None,
                  generator=None)


def def_clear_definitional_action():
    ARG_LOC = "$location"

    precond_0 = None
    precond_1: Set[Tuple] = set()
    for obj in ALL_OBJECTS:
        # TODO: hacky way to declare region
        # 0 means out of ...
        # 1 means in ...
        precond_1.add((PREDICATES.IN, obj, 0, (ARG_LOC,)))

    effect_add: Set[Tuple] = set()
    effect_add.add((PREDICATES.GRID_CLEAR, ARG_LOC))
    effect_delete = precond_1
    return Action(name="Clear",
                  precond=[precond_0, precond_1],
                  add=effect_add,
                  delete=effect_delete,
                  arguments=(ARG_LOC,),
                  choose=None,
                  generator=None)


def def_in_definitional_action():
    ARG_OBJECT = "$OBJECT"
    ARG_FLAG = "$flag"
    ARG_REGION = "$region"
    CHOOSE_LOCATION = "$location"

    precond_0: Set[Tuple] = set()
    precond_0.add((PREDICATES.OBJ_LOC, ARG_OBJECT, CHOOSE_LOCATION))

    effect_add: Set[Tuple] = set()
    effect_add.add((PREDICATES.IN, ARG_OBJECT, ARG_FLAG, ARG_REGION))

    def _gen(binding):
        flag = binding[ARG_FLAG]
        position_min, position_max = region_to_range(binding[ARG_REGION])

        if flag:
            for i in range(position_min, position_max):
                yield (i,)
        else:
            for i in ALL_GRIDS:
                if i not in [
                        grid for grid in range(position_min, position_max)
                ]:
                    yield (i,)

    return Action(name="In",
                  precond=[precond_0],
                  add=effect_add,
                  delete=None,
                  arguments=(ARG_OBJECT, ARG_FLAG, ARG_REGION),
                  choose=(CHOOSE_LOCATION,),
                  generator=_gen)


ACTION_SCHEMES: List[Action] = [
    def_cook_action(),
    def_wash_action(),
    def_pick_place_action(),
    def_clear_definitional_action(),
    def_clear_region_definitional_action(),
    def_in_definitional_action()
]
