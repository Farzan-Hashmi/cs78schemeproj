"""
Name: Farzan Hashmi, Ngoc Pham, Kartikey Sharma
Project Name: Scheme Interpreter
Project Purpose: Read and Execute Scheme Code. This class works on executing code and doing actual operations
"""
import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4

    (* 3 4 (- 5 2) 1)
    >>> expr = read_line('(* 3 4 (- 5 2) 1)')
    >>> expr
    Pair('*', Pair(3, Pair(4, Pair(Pair('-', Pair(5, Pair(2, nil))), Pair(1, nil)))))
    >>> scheme_eval(expr, create_global_frame())
    36
    """


    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3

        # go to the deepest level of the expression
        #   Pair('+', Pair(2, Pair(2, nil))) for example
        # This gives the evaluation of the first argument in args
        operation = scheme_eval(first, env)
        # This recursive call ensures that all arguments in args will be called
        args = rest.map(lambda arg: scheme_eval(arg, env))
        return scheme_apply(operation, args, env)
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        # convert args to a Python list
        # args is a Pair Object
        # args.first is the first element of the Pair
        # args.rest is the rest of the Pair
        "*** YOUR CODE HERE ***"
        # Add all values of args to the args_list, then add the environment if it needs the environment.
        # args_list is the list of arguments, in order, to apply
        args_list = []
        while args is not nil:
            args_list.append(args.first)
            args = args.rest
        if procedure.need_env:
            args_list.append(env)  
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            # Return all the ran procedures unless it's not possible
            return procedure.py_func(*args_list)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # create new child frame
        # after making child frame, evaluate the body of the frame.
        nextFrame = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, nextFrame)

        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        env = procedure.make_child_frame(args, env)
        return eval_all(procedure.body, env)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # Check if theres anything to evaluate
    if(expressions==nil):
        return None
    toReturn = nil     
    currExpression = expressions
    # currExpression updates every time to become smaller, while toReturn updates to contain
    # the evaluation of the element that currExpression removes.
    for i in range(0, len(expressions)):
        if(currExpression == nil):
            break
        toReturn = scheme_eval(currExpression.first, env)
        currExpression = currExpression.rest
    return toReturn


        

    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC
    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
