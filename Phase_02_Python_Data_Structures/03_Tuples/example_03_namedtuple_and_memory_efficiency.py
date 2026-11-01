"""
Topic 03: Tuples
Example 03: `collections.namedtuple` and Memory Footprint Comparison

Demonstrates how `namedtuple` adds readable attribute access (`.lat`, `.lon`)
to standard tuples without extra per-instance dictionary overhead, and compares
memory usage between `tuple` and `list`.
"""

from collections import namedtuple
import sys

GeoPoint = namedtuple("GeoPoint", ["city", "lat", "lon"])


def main() -> None:
    print("=== 1. Readable Records with collections.namedtuple ===")
    hq = GeoPoint(city="Bengaluru", lat=12.9716, lon=77.5946)
    print(f"NamedTuple repr : {hq}")
    print(f"By Attribute    : city={hq.city}, lat={hq.lat}, lon={hq.lon}")
    print(f"By Index [0]    : {hq[0]} (100% backward-compatible with tuple!)")

    print("\n=== 2. Memory Footprint: tuple vs list ===")
    sample_tuple = tuple(range(1000))
    sample_list = list(range(1000))
    tuple_bytes = sys.getsizeof(sample_tuple)
    list_bytes = sys.getsizeof(sample_list)
    print(f"1000-element tuple size : {tuple_bytes} bytes")
    print(f"1000-element list size  : {list_bytes} bytes")
    print(f"Tuple uses fewer bytes? : {tuple_bytes < list_bytes}")


if __name__ == "__main__":
    main()
