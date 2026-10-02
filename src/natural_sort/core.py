"""Natural sort key function and sorted-list helper.

A natural sort orders strings so that numeric substrings are compared by their
integer value rather than lexicographically. This is what people usually want
when sorting filenames or version-like strings: file2 before file10.

Interpretation chosen for this library (stated plainly so the tests and users
know exactly what they get):

* Each string is split into alternating alphabetic and numeric chunks. A chunk
  is a maximal run of digits or a maximal run of non-digits. Empty chunks never
  appear because the regex alternation consumes at least one character per
  match.
* Leading zeros on a numeric chunk do not affect the numeric value
  (0-padding is ignored for ordering). file007 and file7 compare equal on the
  numeric field, and the surrounding text breaks the tie, so file07 sorts
  before file7 only if the surrounding text also sorts before it.
* The alphabetic chunks are compared case-sensitively. Natural sort libraries
  differ on this; some lower-case, some don't. We don't lower-case because doing
  so would silently change the order of inputs like Foo and foo, and that is
  the caller's decision to make, not ours. Call str.lower on your inputs first
  if you want case-insensitive ordering.
* Input may be any object with a sensible str() representation; non-str inputs
  are stringified so the function can be used directly as a list sort key on
  mixed lists. None sorts as the string 'None'.
"""

import re

# One match per chunk: either a maximal run of digits or a maximal run of
# non-digits. Using findall (not split) means we never produce empty chunks,
# which avoids an awkward special case in the comparison below.
_CHUNK_RE = re.compile(r"(\d+|\D+)")


def _chunks(s):
    """Yield (is_digit, value) pairs for each chunk of s.

    is_digit is a bool; value is the original substring for non-digit chunks,
    or the integer value for digit chunks.
    """
    for chunk in _CHUNK_RE.findall(s):
        # findall with one capturing group returns the captured text directly,
        # so chunk is a str of length >= 1.
        if chunk[0].isdigit():
            yield True, int(chunk)
        else:
            yield False, chunk


def natural_sort_key(value):
    """Return a sort key for natural ordering of value.

    Use as key=natural_sort_key with list.sort or sorted. The returned object
    is a tuple of (bool, int|str) pairs. It is comparable with other keys
    produced by this function; comparing it with anything else is undefined.

    Comparing two such tuples element-wise is the natural order: chunk types
    are compared first (digit chunks sort before non-digit chunks at the same
    position) and then chunk values. Chunk type is included in each tuple
    element so that a pure-digit chunk never attempts to compare against a
    pure-str chunk, which would raise TypeError.
    """
    s = value if isinstance(value, str) else str(value)
    return tuple(_chunks(s))


def natural_sorted(iterable, *, key=None, reverse=False):
    """Return a new list of the items of iterable in natural order.

    If key is given it is applied to each item first, and natural ordering is
    applied to the key's result. key may be None to sort the items themselves.
    reverse reverses the final order, as with sorted().
    """
    if key is None:
        effective = natural_sort_key
    else:
        effective = lambda item: natural_sort_key(key(item))
    return sorted(iterable, key=effective, reverse=reverse)
