from typing import Optional, Set, Tuple, Dict

# fluent is just a tuple
# first element is str: the name of the fluent
# the rest are arguments of the fluent


def fluent_holds_at(state: Set[Tuple], fluent: Tuple) -> bool:
    '''evaluate whether fluent is true in state, state is not modified
    
    Example:
        >>> s = set()
        >>> s.add(("done", ))
        >>> s.add(("clean", "obj_a"))
        >>> s.add(("in", "obj_a", "sink"))
        >>> s.add(("dist", "home", "park", 8))
        >>> s.add(("dist", "park", "home", 8))
        >>> 
        >>> fluent_holds_at(s, ())
        False
        >>> fluent_holds_at(s, ("clean", "obj_a"))
        True
        >>> fluent_holds_at(s, ("clean", "obj_b"))
        False
        >>> fluent_holds_at(s, ("dist", "park", "home", 8))
        True
        >>> s == s
        True
    '''

    return fluent in state


def fluent_to_string(fluent: Tuple) -> str:
    arguments_str = ""
    if len(fluent) > 1:
        arguments_str = "(" + ", ".join([str(x) for x in fluent[1:]]) + ")"
    return "{}{}".format(fluent[0], arguments_str)

# an expression is a fluent that could have some argument unbinded
# the unbinded argument is denotes by a string that starts with "$"
# for example, in ("On", "$a", "stove"), $a is unbinded
# unifying two expressions returns the argument binding to make the two
# expressions equal to each other (if such binding exists)
def unify(expression1: Tuple,
          expression2: Tuple) -> Tuple[bool, Optional[dict], Optional[dict]]:
    # assume expressions have at least length 1
    # assume the first element is a string
    # assume the first element doesn't start with '$'
    if expression1[0] != expression2[0]:
        return False, None, None
    binding1 = {}
    binding2 = {}
    for v1, v2 in zip(expression1[1:], expression2[1:]):
        success, d1, d2 = unify_helper(v1, v2)
        if not success:
            return False, None, None
        if d1:
            d1 = merge_variable_bindings(binding1, d1)
            if d1 is None:
                return False, None, None
            binding1 = d1
        if d2:
            d2 = merge_variable_bindings(binding2, d2)
            if d2 is None:
                return False, None, None
            binding2 = d2
    if not binding1:
        binding1 = None
    if not binding2:
        binding2 = None
    return True, binding1, binding2


def unify_helper(val1, val2) -> Tuple[bool, Optional[dict], Optional[dict]]:

    # if not val1 or not val2:  # val1 or 2 is empty
    #     if not val1 and not val2:  # both empty
    #         return True, None, None
    #     else:
    #         return False, None, None
    is_val1_str = type(val1) == str
    is_val2_str = type(val2) == str
    is_val1_var = is_val1_str and val1.startswith('$')
    is_val2_var = is_val2_str and val2.startswith('$')

    if is_val1_var and is_val2_var:
        # TODO: check if there's a linking conflict, like p($a, b, $a), p($b, $b, c)
        return True, None, None
    elif is_val1_var:
        return True, {val1: val2}, None
    elif is_val2_var:
        return True, None, {val2: val1}
    else:
        return val1 == val2, None, None


# ref: https://stackoverflow.com/questions/31323388/merging-two-dicts-in-python-with-no-duplication-permitted
def merge_variable_bindings(d1: Dict, d2: Dict) -> Optional[dict]:
    return (None if any(d1[k] != d2[k] for k in d1.keys() & d2) else {
        **d1,
        **d2
    })


# bind the argument in an expression
# apply_binding(('on', '$arg1', 'stove'), {'$arg1': 'obj_A', "$arg,....}) => ('on', 'obj_A', 'stove')
def apply_binding(expression: Tuple, binding: dict) -> Tuple:
    bind = list(expression)
    binding_key = list(binding.keys())
    binding_value = list(binding.values())
    for i in bind:
        #search for the tuple element in the expression
        if type(i) is tuple:
            original = i
            original = list(original)
            for j in range(len(binding_key)):
                if binding_key[
                        j] in i:  #loop through the binding dictionary keys
                    for a in range(
                            len(original)
                    ):  #loop through the tuple inside the expression
                        if original[a] == binding_key[
                                j]:  #find out the key with the same name as the element inside the tuple
                            original[a] = binding_value[
                                j]  #replace the tuple element with the binding values with corresponding key names
            for q in range(len(bind)):
                #loop through the expression to locate the tuple and replace the new value
                if bind[q] == i:
                    bind[q] = tuple(original)
    #replacing elements with types other than tuple
    for i in range(len(bind)):
        if bind[i] in binding_key:
            name = str(bind[i])
            bind[i] = binding[name]

    return tuple(bind)


def apply_binding_to_set_of_fluents(expressions: Optional[Set[Tuple]],
                                    binding: Dict) -> Optional[Set[Tuple]]:
    if not expressions:
        return None
    else:
        binded_expressions = set()
        for expression in expressions:
            binded_expressions.add(apply_binding(expression, binding))
        return binded_expressions


def main():
    if __name__ == "__main__":
        import doctest
        doctest.testmod()
