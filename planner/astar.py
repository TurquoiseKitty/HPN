from collections import deque
from typing import Callable, Deque, Dict, Generic, Hashable, List, Set, Tuple, Optional, TypeVar
import heapq
import logging

ActionType = TypeVar("ActionType")
StateType = TypeVar("StateType", bound=Hashable)
GoalType = TypeVar("GoalType")


class SearchTreeNode(Generic[ActionType, StateType]):
    estimated_total_cost: float  # heap sort by the first field in tuple
    base_cost: float
    node_id: int
    parent_node_id: Optional[int]
    content: Tuple[Optional[ActionType], StateType]

    def __init__(self, estimated_total_cost: float, base_cost: float,
                 node_id: int, parent_node_id: Optional[int],
                 content: Tuple[Optional[ActionType], StateType]) -> None:
        self.estimated_total_cost = estimated_total_cost
        self.base_cost = base_cost
        self.node_id = node_id
        self.parent_node_id = parent_node_id
        self.content = content

    def __lt__(self, other):
        return self.estimated_total_cost < other.estimated_total_cost


# astar doesn't need to differentiate between forward and backward search
def astar(
    # yapf: disable
    starting_state: StateType,
    goal: GoalType,
    generate_successors: Callable[[StateType], List[Tuple[Optional[ActionType],
                                                          StateType]]],
    heuristic_func: Callable[[StateType, GoalType], int],
    goal_test: Callable[[StateType, GoalType], bool]
    # yapf: enable
) -> Tuple[bool, Optional[Deque], Optional[Deque]]:
    """A* search algorithm

    Args:
        current_state (StateType): where we are now
        goal (GoalType): where we want to go
        operators (Dict[str, planner.action.Action]): all the actions that we can do
        generate_successors (Callable): where we could go given the actions
        heuristic_func (Callable[[StateType, GoalType], int]): estimate how much further we need to go
        goal_test (Callable[[StateType, GoalType], bool]): are we there yet

    Returns:
        Tuple[bool, Optional[Deque], Optional[Deque]]: if we can find a path, what is the path
    """
    open_list: List[SearchTreeNode] = []

    # hash set supports quickly checking if a state is visited
    visited_search_state_set: Set[StateType] = set()

    # dict supports quickly looking up a search node by node id
    visisted_search_node_dict: Dict[int, SearchTreeNode] = {}
    new_node_id_counter = 0

    initial_search_node = SearchTreeNode(heuristic_func(starting_state, goal),
                                         0, new_node_id_counter, None,
                                         (None, starting_state))
    new_node_id_counter += 1
    heapq.heappush(open_list, initial_search_node)

    while open_list:  # more possibilities to explore in the open list
        current_node = open_list[0]  # node with smallest estimated_total_cost
        heapq.heappop(open_list)

        current_node_state: StateType = current_node.content[1]

        visited_search_state_set.add(current_node_state)
        visisted_search_node_dict[current_node.node_id] = current_node

        # check if we've reached the goal
        if goal_test(current_node_state, goal):
            # success! back trace to find the path
            action_path: Deque = deque([current_node.content[0]])
            state_path: Deque = deque([current_node.content[1]])
            parent_node_id = current_node.parent_node_id
            while parent_node_id is not None:
                current_node = visisted_search_node_dict[parent_node_id]
                action_path.appendleft(current_node.content[0])
                state_path.appendleft(current_node.content[1])
                parent_node_id = current_node.parent_node_id
            return True, action_path, state_path
        else:
            new_children = generate_successors(current_node_state)
            for new_child in new_children:
                new_child_state: StateType = new_child[1]
                if new_child_state in visited_search_state_set:
                    continue
                # todo: cost not always 1
                child_base_cost = current_node.base_cost + 1
                estimated_child_total_cost = child_base_cost + heuristic_func(
                    new_child_state, goal)
                is_current_node_found_in_open_list = False
                for open_list_node in open_list:
                    # todo: this == icon might not plausable
                    if open_list_node.content[1] == new_child_state:
                        old_estimate = open_list_node.estimated_total_cost
                        if estimated_child_total_cost < old_estimate:
                            open_list_node.parent_node_id = current_node.node_id
                            open_list_node.base_cost = child_base_cost
                            open_list_node.estimated_total_cost = estimated_child_total_cost

                            # modify the action in the open_list_node
                            open_list_node.content = new_child
                        is_current_node_found_in_open_list = True
                        break
                if not is_current_node_found_in_open_list:
                    new_search_node = SearchTreeNode(estimated_child_total_cost,
                                                     child_base_cost,
                                                     new_node_id_counter,
                                                     current_node.node_id,
                                                     new_child)
                    new_node_id_counter += 1
                    heapq.heappush(open_list, new_search_node)

    logging.warning("fail!")
    return False, None, None
