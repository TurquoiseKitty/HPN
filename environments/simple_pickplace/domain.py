from enum import Enum
import string
# all grids 0,1,2,3,4
NUM_GRIDS = 5
ALL_GRIDS = tuple(range(NUM_GRIDS))
WASH_GRID = ALL_GRIDS[1]
COOK_GRID = ALL_GRIDS[2]

NUM_OBJECTS = 3
ALL_OBJECTS = tuple(string.ascii_lowercase[:NUM_OBJECTS])


class PREDICATES(str, Enum):
    IN = "in"
    CLEAN = "clean"
    COOKED = "cooked"
    OBJ_LOC = "obj_loc"  # ("obj_loc", object_name, location)
    GRID_CLEAR = "grid_clear"
    REGION_CLEAR = "region_clear"
