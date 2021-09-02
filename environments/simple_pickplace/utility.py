from environments.simple_pickplace.domain import PREDICATES
# test if state satisfies goal
# we replace this by another goal_test

def goal_test(goal, state):
    goal = list(goal)
    state = list(state)
    remove_index = []
    for i in range(len(goal)):
        flu = goal[i]
        if flu[0] == PREDICATES.GRID_CLEAR:
            grid = flu[1]
            for state_flu in state:
                if state_flu[0] == PREDICATES.OBJ_LOC and state_flu[2] == grid:
                    return False

            remove_index.append(i)

    goal_shrink = []
    for j in range(len(goal)):
        if j not in remove_index:
            goal_shrink.append(goal[j])
    goal = goal_shrink

    goal = set(goal)
    state = set(state)

    for flu in goal:
        if flu[0] == PREDICATES.CLEAN and flu not in state:
            return False

    for flu in goal:
        if flu[0] == PREDICATES.COOKED and flu not in state:
            return False

    return goal.issubset(state)

# we replace this by another is_contradiction

def is_contradiction(goal):
    goal = list(goal)
    clear_requirement = []
    for i in range(len(goal)):
        if goal[i][0] == PREDICATES.GRID_CLEAR:
            clear_requirement.append(i)

    for clear in clear_requirement:
        grid = goal[clear][1]
        for fluent in goal:
            if fluent[0] == PREDICATES.OBJ_LOC and fluent[2] == grid:
                return True

    # there cannot be two locate at
    foods_location = {}
    for flu in goal:
        if flu[0] == PREDICATES.OBJ_LOC:
            food_name = flu[1]
            loc = flu[2]
            if food_name not in foods_location.keys():
                foods_location[food_name] = loc
            else:
                if foods_location[food_name] != loc:
                    return True

    return False

def check_consistency(subgoal):
    return not is_contradiction(subgoal)

