"""
Topic 03 - Data Structures: Question 3
Problem: Immutable Geospatial Navigation System using namedtuples and tuples.
"""

from collections import namedtuple
import math

# 1. Named Tuple Definition
Waypoint = namedtuple("Waypoint", ["name", "latitude", "longitude", "elevation_m"])

alpha = Waypoint(name="Alpha", latitude=37.7749, longitude=-122.4194, elevation_m=15.0)
bravo = Waypoint(name="Bravo", latitude=37.7833, longitude=-122.4167, elevation_m=22.5)
charlie = Waypoint(name="Charlie", latitude=37.7900, longitude=-122.4000, elevation_m=8.0)

print(f"Waypoint Alpha: {alpha}")
print(f"Positional Access: Name='{alpha[0]}', Elevation={alpha[3]} m")

# 2. Immutability Verification
try:
    alpha.latitude = 45.0  # type: ignore
except AttributeError as err:
    print(f"Immutability Verified: Caught AttributeError on attempted reassignment: {err}")

# 3. Composite Dictionary Keys
weather_map = {
    (37.77, -122.42): "Clear Sky",
    (37.78, -122.41): "Foggy",
    (37.79, -122.40): "Partly Cloudy",
}

query_coord = (37.77, -122.42)
print(f'Dictionary Key Lookup for {query_coord}: "{weather_map.get(query_coord, "Unknown")}"')

try:
    # Attempting to use a mutable list as dictionary key
    invalid_map = {}
    invalid_map[[37.77, -122.42]] = "Error expected"  # type: ignore
except TypeError as err:
    print(f"Unhashable List Key Verified: Caught TypeError on list dictionary key: {err}")

# 4. Tuple Packing, Unpacking & Arithmetic
route_leg_1 = (alpha, bravo)
route_leg_2 = (charlie,)
full_route = route_leg_1 + route_leg_2

print(f"Total Route Waypoint Count: {len(full_route)} waypoints")

for i in range(len(full_route) - 1):
    wp1 = full_route[i]
    wp2 = full_route[i + 1]
    dist = math.sqrt((wp2.latitude - wp1.latitude) ** 2 + (wp2.longitude - wp1.longitude) ** 2)
    print(f"Leg {i+1} ({wp1.name} -> {wp2.name}): Delta-Coord Distance = {dist:.5f}")

alert_tuple = ("PULL_UP",) * 3
print(f"Repeated Alert Tuple: {alert_tuple}")
