# %%
from collections import deque
from IPython import get_ipython

ipython = get_ipython()
if ipython is not None:
    ipython.magic("load_ext autoreload")
    ipython.magic("autoreload 2")

# %%
import logging

logging.basicConfig(
    format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.CRITICAL)

# %%
from typing import Deque, Set, Tuple

from planner.fluent import fluent_to_string
from planner.state import state_to_str
from planner.hpn.hpn import HPN

from environments.simple_pickplace.domain import PREDICATES

# from environments.simple_pickplace.problog_machine import check_consistency, goal_test
from environments.simple_pickplace.problog_machine import check_consistency, goal_test

from environments.simple_pickplace.action_schemes import ACTION_SCHEMES

# define the problem
current_state: Set[Tuple] = set()
current_state.add((PREDICATES.OBJ_LOC, "a", 2))
current_state.add((PREDICATES.OBJ_LOC, "b", 1))

# current_state.add((PREDICATES.OBJ_LOC, "a", 0))
# current_state.add((PREDICATES.OBJ_LOC, "b", 1))
# current_state.add((PREDICATES.OBJ_LOC, "c", 2))
logging.info(f"Initial State: \n{state_to_str(current_state)}")

goal: Set[Tuple] = set()
goal.add((PREDICATES.COOKED, "a"))
goal.add((PREDICATES.COOKED, "b"))
logging.info(f"Goal: \n{state_to_str(goal)}")

hpn = HPN(ACTION_SCHEMES,
          check_consistency=check_consistency,
          check_current_world_state_satisfy_goal=goal_test)

# %%
import graphviz
import matplotlib.pyplot

from environments.simple_pickplace.domain import ALL_OBJECTS, WASH_GRID, COOK_GRID, NUM_GRIDS

from planner.hpn.abstraction_level_dict import get_action_abstraction_level


class OBJ_PROPERTY:

    def __init__(self, name):
        self.name = name
        self.loc = -1
        self.clean = False
        self.cooked = False


def world_visualizer(current_world_state):
    '''DO NOT MODIFY current_world_state'''
    # all what we care are :
    # where are wash and cook grids
    # locations of all objects
    # whether each of them are washed or cooked

    print("\n")
    print("WASH_GRID : " + str(WASH_GRID))
    print("COOK_GRID : " + str(COOK_GRID))
    obj_list = []
    for name in ALL_OBJECTS:
        obj_list.append(OBJ_PROPERTY(name))
    for flu in current_world_state:
        if flu[0] == PREDICATES.CLEAN:
            name = flu[1]
            for obj in obj_list:
                if obj.name == name:
                    obj.clean = True
                    break
        elif flu[0] == PREDICATES.COOKED:
            name = flu[1]
            for obj in obj_list:
                if obj.name == name:
                    obj.cooked = True
                    break

        elif flu[0] == PREDICATES.OBJ_LOC:
            name = flu[1]
            grid = flu[2]
            for obj in obj_list:
                if obj.name == name:
                    obj.loc = grid
                    break

    grid_demo = ["_"] * NUM_GRIDS
    for obj in obj_list:
        name = obj.name
        grid = obj.loc
        grid_demo[grid] = name
    demo_string = " ".join(grid_demo)
    print(demo_string)
    for obj in obj_list:
        poten_str = ""
        if obj.clean or obj.cooked:
            poten_str = obj.name + " : "
            if obj.clean:
                poten_str += "clean "
            if obj.cooked:
                poten_str += "cooked "
        if poten_str != "":
            print(poten_str)
    print("\n")


def world_executor(current_world_state, action):
    logging.info(f"Executing Action: {action.action_signature}")
    current_world_state = current_world_state if action.delete == None else current_world_state - action.delete
    current_world_state = current_world_state if action.add == None else current_world_state | action.add
    logging.info(f"New World State: \n{state_to_str(current_world_state)}")

    return current_world_state


import time
from pathlib import Path


class PlanVisualizer:

    def __init__(self) -> None:
        self.graph = graphviz.Digraph()
        self.plan_node_index_counter: int = 1
        self.action_node_index_counter: int = 1
        self.parent_list = deque()

        self.start_time = time.time()
        self.save_counter = 1
        self.base_path = "results/graph"
        Path("results").mkdir(parents=True, exist_ok=True)

    def _get_new_parent(self):
        parent_abs_action, new_goal = self.parent_list.popleft()
        node_name = f"plan{self.plan_node_index_counter}"
        expression = f"Plan {self.plan_node_index_counter}\n {state_to_str(new_goal)}"
        self.plan_node_index_counter += 1

        self.graph.node(name=node_name,
                        label=expression,
                        shape='box',
                        color='Blue')

        if parent_abs_action is not None:
            self.graph.edge(parent_abs_action, node_name)

        return node_name

    def __call__(self, action_path, state_path, abstraction_level_dict):
        '''DO NOT MODIFY action_path, state_path, abstraction_level_dict'''
        logging.info(">>> Constructed Plan >>>")
        print(f"Time Spent: {time.time() - self.start_time}")
        print(f"Plan Length: {len(action_path)}")

        if not self.parent_list:
            self.parent_list.append((None, state_path[-1]))

        parent_plan_node_name = self._get_new_parent()

        goals_to_plan_in_future = deque()
        for action, subgoal in zip(action_path, state_path):
            if action is not None:
                action_signature = action.action_signature
                logging.info(f"Action: {action_signature}")

                abstract_level = get_action_abstraction_level(
                    abstraction_level_dict, action)

                new_action_node_name = f'action{self.action_node_index_counter}'
                self.action_node_index_counter += 1
                is_action_primitive = action.is_primitive(abstract_level)
                action_node_color = "Green" if is_action_primitive else 'Red'

                new_action_node_label = action_signature.replace('\"', "")
                self.graph.node(
                    name=new_action_node_name,
                    label=f'A{abstract_level}:{new_action_node_label}',
                    shape='box',
                    color=action_node_color)
                self.graph.edge(parent_plan_node_name, new_action_node_name)

                if not is_action_primitive:
                    goals_to_plan_in_future.appendleft(
                        (new_action_node_name, subgoal))

            else:
                logging.info(action)
            logging.info(f"Subgoal: \n{state_to_str(subgoal)}")

        self.parent_list.extendleft(goals_to_plan_in_future)

        self._save_graph()
        self.start_time = time.time()

        return

    def _save_graph(self):
        filename = f"{self.base_path}{self.save_counter}"

        self.graph.render(filename=filename)
        # with open(filename, "w") as graph_file:
        #     graph_file.write(self.graph.source)
        print(f"Saved Plan Graph: {self.save_counter}")
        self.save_counter += 1


world_visualizer(current_state)
plan_visualizer = PlanVisualizer()
hpn_plan = hpn(current_state, goal, debug_func=plan_visualizer)

current_planned_action = next(hpn_plan)
try:
    while current_planned_action is not None:
        current_state = world_executor(current_state, current_planned_action)
        world_visualizer(current_state)
        current_planned_action = hpn_plan.send(current_state)
except StopIteration:
    pass

# %%
# plan_visualizer.graph

# %%
# IF_SAVE = True
# graph_filename = 'graph_file.dot'

# if IF_SAVE:
#     with open(graph_filename, "w") as graph_file:
#         graph_file.write(plan_visualizer.graph.source)

# %%
