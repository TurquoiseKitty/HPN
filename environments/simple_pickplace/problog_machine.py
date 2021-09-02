import problog
import problog.logic
from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable
from environments.simple_pickplace.domain import ALL_GRIDS, ALL_OBJECTS, PREDICATES
from environments.simple_pickplace.action_schemes import region_to_range


def problog_analyser(model, target):

    # print("-------------------------MODEL----------------------")
    # print(model)
    # print(target)
    # print(model)
    p = PrologString(model)
    query_result = get_evaluatable().create_from(p).evaluate()
    # print("--------------FINISHED ANALYSING---------------------")
    temp_term = problog.logic.Term(target)
    # print(query_result[temp_term])

    return query_result[temp_term]


# for k, v in query_result.items():
#     print(type(k))


def create_background():
    model_background = "\n\n"
    for grid in ALL_GRIDS:
        model_background += "loc(" + str(grid) + ").\n"
    model_background += "\n"
    for obj in ALL_OBJECTS:
        model_background += "obj(" + obj + ").\n"
    model_background += "\n"
    num_grid = len(ALL_GRIDS)
    model_background += str(1 / num_grid) + "::at(X," + str(ALL_GRIDS[0]) + ")"
    for i in range(1, num_grid):
        model_background += ";" + str(1 / num_grid) + "::at(X," + str(
            ALL_GRIDS[i]) + ")"
    model_background += " :- obj(X)."
    model_background += "\n"
    model_background += """
1/2::clean(X) :- obj(X).
1/2::cooked(X) :- obj(X),clean(X).

grid_occupied(Grid) :- loc(Grid), obj(X), at(X,Grid).
grid_clear(Grid) :- \+grid_occupied(Grid).
region_occupied(REGION_MIN, REGION_MAX) :- loc(Grid), obj(X), at(X,Grid), REGION_MIN @=< Grid, REGION_MAX @> Grid.
region_clear(REGION_MIN, REGION_MAX) :- \+region_occupied(REGION_MIN, REGION_MAX).
in(X,1,REGION_MIN,REGION_MAX) :- loc(Grid), obj(X), at(X,Grid), REGION_MIN @=< Grid,  Grid @< REGION_MAX.
in(X,0,REGION_MIN,REGION_MAX) :- \+in(X,1,REGION_MIN,REGION_MAX).

confli :- at(X,Grid),at(Y,Grid),obj(X),obj(Y),X \= Y,loc(Grid).
evidence(\+confli).

"""
    return model_background


def create_fluent(fluentset):
    fluent_expression = ""
    for fluent in fluentset:
        if fluent[0] == PREDICATES.IN:
            min_pos, max_pos = region_to_range(fluent[3])
            fluent_expression += "in(" + fluent[1] + "," + str(
                fluent[2]) + "," + str(min_pos) + "," + str(max_pos) + "),"

        if fluent[0] == PREDICATES.CLEAN:
            fluent_expression += "clean(" + fluent[1] + "),"
        elif fluent[0] == PREDICATES.COOKED:
            fluent_expression += "cooked(" + fluent[1] + "),"
        elif fluent[0] == PREDICATES.OBJ_LOC:
            fluent_expression += "at(" + fluent[1] + "," + str(fluent[2]) + "),"
        elif fluent[0] == PREDICATES.GRID_CLEAR:
            fluent_expression += "grid_clear(" + str(fluent[1]) + "),"

        elif fluent[0] == PREDICATES.REGION_CLEAR:
            min_pos, max_pos = region_to_range(fluent[1])
            fluent_expression += "region_clear(" + str(min_pos) + "," + str(
                max_pos) + "),"

    fluent_expression = fluent_expression[:-1]
    return fluent_expression


def is_contradiction(goal):
    if len(goal) == 0:
        return False
    model = create_background()
    goal = create_fluent(goal)
    model += "\ngoal :- " + goal + "."
    model += "\nquery(goal)."
    if problog_analyser(model, "goal") < 1e-4:
        return True
    return False


def goal_test(goal, state):
    if len(goal) == 0:
        return True
    model = create_background()
    state_expression = create_fluent(state)
    goal_expression = create_fluent(goal)
    model += "\nstate :- " + state_expression + "."
    model += "\nevidence(state)."
    model += "\ngoal :- " + goal_expression + "."
    model += "\nquery(goal)."
    # print(model)

    if problog_analyser(model, "goal") < 1 - 1e-4:
        return False
    return True


def check_consistency(subgoal):
    return not is_contradiction(subgoal)


if __name__ == "__main__":
    pass