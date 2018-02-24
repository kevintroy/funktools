"""
A few higher-order functions to help learn how certain libraries work and 
facilate doing stupid hacky stuff with data.

These will not be super-fast like numpy functions, so in general you're
better off looking at the numpy docs first to see if there's an optional
WHERE argument to an np.function that will yield the same result in 1/1000th
of the time.
"""
from functools import partial
import numpy as np
import operator as op


def is_error(f, x):
    """
    Mimics Excel ISERROR function
    Returns False if f(x) returns any value
    Returns True if f(x) raises an error

    To implement in Pandas:
    [series].apply(partial(is_error, YOUR FUNCTION HERE))
    """
    try:
        f(x)
        return False
    except:
        return True

assert is_error(float, "abc")

int_error = partial(is_error, int)
assert not int_error("3")
assert not int_error(3.0)
assert int_error("abc")
assert int_error("3.0")   # int cannot cast floats-as-strings directly
assert int_error(np.nan)  # np.NaN cannot be stored as an int, b/c reasons

def if_error(f, x, upon_error):
    """
    Mimics Excel IFERROR functionality.
    If you're using this, you're probably doing Python wrong.
    (If you're using this with numpy/pandas, check the numpy WHERE argument
    first.)
    But sometimes it's useful.
    Like maybe you'd like to ignore unicode errors for a while so you can 
    get a sense of the data.  Or setting log(0) to 0 won't ruin your plot.
    To .apply() in Pandas, use together with partial() or a lambda expression.

    Upon_error can be a value, or g(x).
    """
    try:
        return f(x)
    except:
        return upon_error

# use case for IFERROR:  you want to scan an iterable of mixed data 
# types, and just plain find the ones that match a string, w/out
# worrying about the fact that some are np.NaN or an int or something
assert not if_error(partial(op.contains, 1), "spam", False) 
#^^ exception b/c float not iterable
assert not if_error(partial(op.contains, "eggs"), 1, False) 
#^^ exception b/c number not converted to string first
assert not if_error(partial(op.contains, "shrubbery"), "ni", False)
#^^ no exception, successfully returns that the condition isn't true
assert if_error(partial(op.contains, "spam"), "pa", False)
#^^ no exception, condition is true

# another use case: you're munging something that has some godawful fixed-
# width format where a certain position in the string is somehow important,
# but not all strings go the full width.
assert if_error(partial(op.getitem, "z"*9), 10, '') == ''
assert if_error(partial(op.getitem, "xyzzy"), 1, '') == 'y'
assert if_error(chr, (op.getitem("xyzzy", 1)), np.nan) == chr('y')
assert np.isnan(if_error(chr, (op.getitem("z"*9, 10), np.nan)))


# TO-DO: var_spammer function
#        plot_spammer
#        stock chart
