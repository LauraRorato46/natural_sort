# natural_sort

A tiny standard-library-only library for sorting strings the way a person expects: file2 before file10.

## Usage

```python
from natural_sort import natural_sorted, natural_sort_key

names = ["file10.txt", "file1.txt", "file2.txt"]
print(natural_sorted(names))
# ['file1.txt', 'file2.txt', 'file10.txt']

names.sort(key=natural_sort_key)
print(names)
# ['file1.txt', 'file2.txt', 'file10.txt']
```

`natural_sort_key(value)` returns a comparable key that can be passed to `list.sort` or `sorted`. `natural_sorted(iterable, *, key=None, reverse=False)` is a convenience wrapper around `sorted` that applies it; `key` is applied to each item before natural ordering, as with `sorted`.

## Why

Plain string sort puts file10 before file2 because it compares character-by-character. Natural sort splits each string into alternating numeric and non-numeric chunks and compares numeric chunks by their integer value. The trade-off is a little more work per comparison in exchange for output that matches what a person scanning a directory listing expects.

## Edges

Comparisons are case-sensitive. `Foo` and `foo` sort by their bytes. Call `str.lower` on your inputs first if you want case-insensitive ordering. Leading zeros on numbers are ignored for the numeric value: `file7` and `file007` have identical sort keys, so they will appear in their input order relative to each other (Python's sort is stable).
