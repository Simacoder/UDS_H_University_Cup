# Megazoo Drone Feeding Optimizer
# Supports Level 1 to Level 4 with deadzone and battery constraints

import math
import json
from typing import List, Tuple
from collections import namedtuple

# === Data Structures ===
Point = namedtuple('Point', ['x', 'y', 'z'])
Storage = namedtuple('Storage', ['x', 'y', 'z', 'diet'])
Enclosure = namedtuple('Enclosure', ['x', 'y', 'z', 'importance', 'diet'])
Deadzone = namedtuple('Deadzone', ['x', 'y', 'r'])

path = 'level1.txt'
# === Utility Functions ===
def distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def horizontal_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def parse_zoo_file(path: str):
    with open(path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    dimensions = eval(lines[0])
    depot = Point(*eval(lines[1]))
    battery_capacity = float(lines[2])
    food_storages = [Storage(*fs[:3], fs[3]) for fs in eval(lines[3])]
    enclosures = [Enclosure(*enc[:3], enc[3], enc[4]) for enc in eval(lines[4])]
    deadzones = [Deadzone(*dz) for dz in eval(lines[5])] if len(lines) > 5 else []

    return dimensions, depot, battery_capacity, food_storages, enclosures, deadzones

def total_path_distance(path: List[Point], z_lift=50) -> float:
    dist = 0
    for i in range(1, len(path)):
        if path[i-1].z == 0 and path[i].z == 50:
            dist += z_lift  # Takeoff
        elif path[i-1].z == 50 and path[i].z == 0:
            dist += z_lift - path[i].z  # Landing
        else:
            dist += distance(path[i-1], path[i])
    return dist

def in_deadzone(p: Point, deadzones: List[Deadzone]) -> bool:
    return any(math.sqrt((p.x - dz.x)**2 + (p.y - dz.y)**2) <= dz.r for dz in deadzones)

def plan_run(depot: Point, storages: List[Storage], enclosures: List[Enclosure], battery: float, deadzones: List[Deadzone]) -> List[List[Tuple[int, int]]]:
    runs = []
    fed = set()

    while True:
        best_score = 0
        best_run = []
        best_type = None

        for storage in storages:
            candidates = [e for e in enclosures if e.diet == storage.diet and (e.x, e.y) not in fed]
            if not candidates:
                continue

            for enc in candidates:
                path = [
                    Point(depot.x, depot.y, 0),
                    Point(storage.x, storage.y, 50),
                    Point(enc.x, enc.y, 0),
                    Point(depot.x, depot.y, 0)
                ]
                td = total_path_distance(path)
                if td > battery:
                    continue
                if any(in_deadzone(p, deadzones) for p in path):
                    continue

                score = enc.importance * 1000 - td
                if score > best_score:
                    best_score = score
                    best_run = path
                    best_type = (enc.x, enc.y)

        if best_run:
            fed.add(best_type)
            runs.append([(p.x, p.y) for p in best_run])
        else:
            break

    return runs

def main(level_file: str, output_file: str):
    dims, depot, battery, storages, enclosures, deadzones = parse_zoo_file(level_file)
    runs = plan_run(depot, storages, enclosures, battery, deadzones)
    with open(output_file, 'w') as f:
        json.dump(runs, f)

# Test code:
# main('level1.txt', 'submission_level1.txt')
