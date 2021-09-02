from typing import Set, Tuple

State = Set[Tuple]


def state_to_str(state: State) -> str:
    r'''
    Just for debugging, print out a state
    sort the fluents first for consistency (could be expensive)
    each line shows one fluent value.

    Example:
        >>> s = set()
        >>> s.add(("done", ))
        >>> s.add(("clean", "obj_a"))
        >>> s.add(("in", "obj_a", "sink"))
        >>> s.add(("dist", "home", "park", 8))
        >>> s.add(("dist", "park", "home", 8))
        >>> print_state(s)
        -----
        clean(obj_a)
        dist(home, park, 8)
        dist(park, home, 8)
        done
        in(obj_a, sink)
        -----
    '''
    s = ""
    for fluent in sorted(state):
        arguments_str = ""
        if len(fluent) > 1:
            arguments_str = "(" + ", ".join([str(x) for x in fluent[1:]]) + ")"
        s += f"{fluent[0]}{arguments_str}\n"
    # return f"\n-----\n{s}-----\n"
    return s


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
