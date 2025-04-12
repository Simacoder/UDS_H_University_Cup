# level4.py - Complete MegaZoo Solver for Level 4

import sys
import math
import json

# === Utility Functions ===
def parse_zoo_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    dimensions = eval(lines[0])
    drone_depot = eval(lines[1])
    battery_capacity = int(lines[2])
    food_storages = eval(lines[3])
    enclosures = eval(lines[4])
    deadzones = eval(lines[5]) if len(lines) > 5 else []

    return {
        'dimensions': dimensions,
        'drone_depot': drone_depot,
        'battery_capacity': battery_capacity,
        'food_storages': food_storages,
        'enclosures': enclosures,
        'deadzones': deadzones,
        'depot_2d': (drone_depot[0], drone_depot[1])
    }

def calculate_distance(p1, p2, flight_height=50):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    vertical = abs(flight_height - z1) + abs(flight_height - z2)
    horizontal = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return vertical + horizontal

def distance_2d(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def intersects_deadzone(p1, p2, deadzones):
    x1, y1 = p1
    x2, y2 = p2
    for x, y, r in deadzones:
        dx, dy = x - x1, y - y1
        line_len = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if line_len == 0:
            return distance_2d((x1, y1), (x, y)) <= r
        udx, udy = (x2 - x1) / line_len, (y2 - y1) / line_len
        t = max(0, min(line_len, dx * udx + dy * udy))
        px, py = x1 + t * udx, y1 + t * udy
        if ((px - x)**2 + (py - y)**2)**0.5 <= r:
            return True
    return False

def evaluate_path(path, zoo_data, fed_enclosures=None):
    if fed_enclosures is None:
        fed_enclosures = set()
    depot = zoo_data['drone_depot']
    food_storages = {(s[0], s[1], s[2]): s[3] for s in zoo_data['food_storages']}
    enclosures_data = {(e[0], e[1], e[2]): (e[3], e[4]) for e in zoo_data['enclosures']}
    deadzones = zoo_data['deadzones']
    current_pos = depot
    current_food = None
    total_distance = 0
    points = 0
    newly_fed = set()

    path_3d = []
    for x, y in path:
        if (x, y) == (depot[0], depot[1]):
            path_3d.append(depot)
        elif (x, y) in [(s[0], s[1]) for s in zoo_data['food_storages']]:
            for s in zoo_data['food_storages']:
                if (x, y) == (s[0], s[1]):
                    path_3d.append((x, y, s[2]))
                    break
        else:
            for e in zoo_data['enclosures']:
                if (x, y) == (e[0], e[1]):
                    path_3d.append((x, y, e[2]))
                    break

    for i in range(len(path_3d) - 1):
        p1, p2 = path_3d[i], path_3d[i+1]
        if intersects_deadzone((p1[0], p1[1]), (p2[0], p2[1]), deadzones):
            return 0, float('inf'), set()
        total_distance += calculate_distance(p1, p2)
        current_pos = p2
        if current_pos in food_storages:
            current_food = food_storages[current_pos]
        if current_pos in enclosures_data and current_pos not in fed_enclosures:
            importance, diet = enclosures_data[current_pos]
            if current_food == diet:
                points += importance * 1000
                newly_fed.add(current_pos)

    return points - total_distance, total_distance, newly_fed

def generate_drone_runs(zoo_data, battery_swaps):
    depot_2d = zoo_data['depot_2d']
    battery = zoo_data['battery_capacity']
    storages_by_diet = {'c': [], 'h': [], 'o': []}
    for s in zoo_data['food_storages']:
        storages_by_diet[s[3]].append(s)
    enclosures_by_diet = {'c': [], 'h': [], 'o': []}
    for e in zoo_data['enclosures']:
        enclosures_by_diet[e[4]].append(e)
    for diet in enclosures_by_diet:
        enclosures_by_diet[diet].sort(key=lambda x: x[3], reverse=True)

    fed = set()
    runs = []

    for _ in range(battery_swaps):
        best_run, best_score, best_fed = None, 0, set()
        for diet in ['c', 'h', 'o']:
            remaining = [e for e in enclosures_by_diet[diet] if (e[0], e[1], e[2]) not in fed]
            if not remaining:
                continue
            for s in storages_by_diet[diet]:
                s_2d = (s[0], s[1])
                cands = []
                for e in remaining:
                    enc_3d = (e[0], e[1], e[2])
                    if calculate_distance((s[0], s[1], s[2]), enc_3d) + calculate_distance(enc_3d, zoo_data['drone_depot']) < battery * 0.9:
                        cands.append(e)
                if not cands:
                    continue
                best = cands[0]
                path = [depot_2d, s_2d, (best[0], best[1]), depot_2d]
                score, dist, new_fed = evaluate_path(path, zoo_data, fed)
                if dist <= battery and score > best_score:
                    best_run, best_score, best_fed = path, score, new_fed

        if best_run:
            runs.append(best_run)
            fed.update(best_fed)
        else:
            break
    return runs

def optimize_route(points, zoo_data):
    if len(points) <= 3:
        return points
    depot = points[0]
    mid = points[1:-1]
    route = [mid.pop(0)]
    while mid:
        nearest = min(mid, key=lambda p: distance_2d(route[-1], p))
        route.append(nearest)
        mid.remove(nearest)
    final = [depot] + route + [depot]
    for i in range(len(final)-1):
        if intersects_deadzone(final[i], final[i+1], zoo_data['deadzones']):
            return points
    return final

def format_output(runs):
    return str(runs).replace(' ', '')

def solve_level4(input_file, output_file):
    zoo_data = parse_zoo_file(input_file)
    runs = generate_drone_runs(zoo_data, battery_swaps=250)
    optimized = [optimize_route(run, zoo_data) for run in runs]
    with open(output_file, 'w') as f:
        f.write(format_output(optimized))
    print(f"Saved to {output_file}")
    score = 0
    fed = set()
    for run in optimized:
        s, d, f = evaluate_path(run, zoo_data, fed)
        fed.update(f)
        score += s
    print(f"Estimated score: {int(score)}")
    print(f"Fed enclosures: {len(fed)}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python level4.py <input_file> <output_file>")
        sys.exit(1)
    solve_level4(sys.argv[1], sys.argv[2])
