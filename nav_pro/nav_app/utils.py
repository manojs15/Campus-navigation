# utils.py

import math

def calculate_euclidean_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_distance_with_waypoints(waypoints):
    """Calculate total distance based on a list of waypoints."""
    total_distance = 0.0
    # Calculate distance between consecutive waypoints
    for i in range(len(waypoints) - 1):
        x1, y1 = waypoints[i]
        x2, y2 = waypoints[i + 1]
        segment_distance = calculate_euclidean_distance(x1, y1, x2, y2)
        total_distance += segment_distance

    return total_distance
