# def f():
#     return [1, 2, 3], [4, 5, 6]
#     # return [1, 2, 3],

# choose_vars = ("$a", "$b")
# # choose_vars = ("$a", )
# vals = f()
# print(vals)

# for val in zip(*vals):
#     print(dict(zip(choose_vars, val)))

# def g(*ab, c, d):
#     print(1000*ab[0]+100*ab[1]+10*c+d)

# t = [1, 2]
# g(*t, 3, 4)
# from typing import Generic, Tuple, Optional, TypeVar

# ActionType = TypeVar("ActionType")
# StateType = TypeVar("StateType")

# class Foo(Generic[ActionType, StateType]):

#     def __init__(self, a: Optional[ActionType], b: StateType) -> None:
#         self.content: Tuple[Optional[ActionType], StateType] = (a, b)

# foo = Foo(1, 1)
# print(foo.content)

# %%
import problog
import problog.logic
from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable

# %%
model = """

grid_occupied(X) :- at(Y, X), loc(X), obj(Y).
grid_clear(X) :- \+grid_occupied(X).

obj(a).
obj(b).

loc(0).
loc(1).
loc(2).
loc(3).

at(a, 1).
at(b, 2).

clean(a).

success :- clean(a), grid_clear(1).

query(success).
"""

p = PrologString(model)
query_result = get_evaluatable().create_from(p).evaluate()

temp_term = problog.logic.Term("success")
print(query_result[temp_term])
# for k, v in query_result.items():
#     print(type(k))

# %%
