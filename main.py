# main.py
# This script solves the MegaZoo problem by parsing the zoo configuration,
filename = 'level1.txt'
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

def calculate_distance(point1, point2, flight_height=50):
    """Calculate distance between two 3D points considering drone movement rules"""
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    
    # Calculate vertical distances (takeoff and landing)
    vertical_distance = abs(flight_height - z1) + abs(flight_height - z2)
    
    # Calculate horizontal distance at flight height
    horizontal_distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    return vertical_distance + horizontal_distance

def intersects_deadzone(point1_2d, point2_2d, deadzones):
    """Check if the line between two 2D points intersects any deadzone"""
    x1, y1 = point1_2d
    x2, y2 = point2_2d
    
    for x, y, radius in deadzones:
        # Vector from start point to circle center
        dx = x - x1
        dy = y - y1
        
        # Length of line segment
        line_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if line_length == 0:  # Same point
            return distance_2d((x1, y1), (x, y)) <= radius
        
        # Unit direction vector
        udx = (x2 - x1) / line_length
        udy = (y2 - y1) / line_length
        
        # Projection of circle center onto line
        t = dx * udx + dy * udy
        t = max(0, min(line_length, t))  # Clamp to line segment
        
        # Closest point on line to circle center
        px = x1 + t * udx
        py = y1 + t * udy
        
        # Distance from closest point to circle center
        closest_dist = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
        
        if closest_dist <= radius:
            return True
            
    return False

def distance_2d(p1, p2):
    """Calculate Euclidean distance between two 2D points"""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def evaluate_path(path, zoo_data, fed_enclosures=None):
    """Evaluate a drone path, returning score, battery usage, and newly fed enclosures"""
    if fed_enclosures is None:
        fed_enclosures = set()
    
    depot = zoo_data['drone_depot']
    food_storages = {(s[0], s[1], s[2]): s[3] for s in zoo_data['food_storages']}
    enclosures_data = {(e[0], e[1], e[2]): (e[3], e[4]) for e in zoo_data['enclosures']}
    deadzones = zoo_data['deadzones']
    flight_height = 50  # Constant flight height
    
    current_pos = depot
    current_food = None
    total_distance = 0
    points = 0
    newly_fed = set()
    
    # Convert 2D path to 3D with proper z-coordinates
    path_3d = []
    for x, y in path:
        # Find the matching point in zoo data to get the z-coordinate
        if (x, y) == (depot[0], depot[1]):
            path_3d.append(depot)
        elif (x, y) in [(s[0], s[1]) for s in zoo_data['food_storages']]:
            for storage in zoo_data['food_storages']:
                if (x, y) == (storage[0], storage[1]):
                    path_3d.append((x, y, storage[2]))
                    break
        else:
            for enclosure in zoo_data['enclosures']:
                if (x, y) == (enclosure[0], enclosure[1]):
                    path_3d.append((x, y, enclosure[2]))
                    break
    
    # Calculate distance and check for deadzone collisions
    for i in range(len(path_3d) - 1):
        p1 = path_3d[i]
        p2 = path_3d[i+1]
        
        # Check for deadzone collision in horizontal movement
        if intersects_deadzone((p1[0], p1[1]), (p2[0], p2[1]), deadzones):
            return 0, float('inf'), set()  # Path intersects deadzone
        
        # Calculate distance for this segment
        segment_distance = calculate_distance(p1, p2)
        total_distance += segment_distance
        
        # Update current position
        current_pos = p2
        
        # Check if we're at a food storage
        if current_pos in food_storages:
            current_food = food_storages[current_pos]
        
        # Check if we're at an enclosure
        if current_pos in enclosures_data and current_pos not in fed_enclosures:
            importance, diet = enclosures_data[current_pos]
            
            # Check if the food matches the diet
            if current_food == diet:
                points += importance * 1000
                newly_fed.add(current_pos)
    
    # Calculate final score
    score = points - total_distance
    
    return score, total_distance, newly_fed

def generate_drone_runs(zoo_data, battery_swaps):
    """Generate optimized drone runs for the given zoo and number of battery swaps"""
    depot_2d = zoo_data['depot_2d']
    battery_capacity = zoo_data['battery_capacity']
    
    # Group food storages by diet
    storages_by_diet = {'c': [], 'h': [], 'o': []}
    for storage in zoo_data['food_storages']:
        x, y, z, diet = storage
        storages_by_diet[diet].append((x, y, z, diet))
    
    # Group enclosures by diet
    enclosures_by_diet = {'c': [], 'h': [], 'o': []}
    for enc in zoo_data['enclosures']:
        x, y, z, importance, diet = enc
        enclosures_by_diet[diet].append((x, y, z, importance, diet))
    
    # Sort enclosures by importance (highest first)
    for diet in enclosures_by_diet:
        enclosures_by_diet[diet].sort(key=lambda x: x[3], reverse=True)
    
    # Track which enclosures have been fed
    fed_enclosures = set()
    drone_runs = []
    
    for _ in range(battery_swaps):
        best_run = None
        best_score = 0
        best_fed = set()
        
        # Try each diet
        for diet in ['c', 'h', 'o']:
            # Skip if no enclosures left for this diet
            remaining_enclosures = [e for e in enclosures_by_diet[diet] 
                                   if (e[0], e[1], e[2]) not in fed_enclosures]
            if not remaining_enclosures:
                continue
            
            # Try each food storage for this diet
            for storage in storages_by_diet[diet]:
                storage_2d = (storage[0], storage[1])
                
                # Start with a simple path: depot -> storage -> feed highest priority enclosures -> depot
                candidate_enclosures = []
                for enc in remaining_enclosures:
                    enc_3d = (enc[0], enc[1], enc[2])
                    
                    # Check if the drone can reach this enclosure and return to depot
                    distance_to_enc = calculate_distance((storage[0], storage[1], storage[2]), enc_3d)
                    distance_to_depot = calculate_distance(enc_3d, zoo_data['drone_depot'])
                    
                    if distance_to_enc + distance_to_depot < battery_capacity * 0.9:  # Leave some margin
                        candidate_enclosures.append(enc)
                
                if not candidate_enclosures:
                    continue
                
                # Start with the most important enclosure
                best_enc = candidate_enclosures[0]
                
                # Create a path: depot -> storage -> enclosure -> depot
                path = [depot_2d, storage_2d, (best_enc[0], best_enc[1]), depot_2d]
                
                # Evaluate the path
                score, distance, newly_fed = evaluate_path(path, zoo_data, fed_enclosures)
                
                # Check if this path is valid (doesn't exceed battery capacity)
                if distance <= battery_capacity and score > 0:
                    # Try to improve the path by adding more enclosures
                    improved = True
                    while improved and len(candidate_enclosures) > 1:
                        improved = False
                        best_insertion = None
                        best_insertion_score = score
                        
                        # Try inserting each remaining enclosure at every possible position
                        for enc in candidate_enclosures[1:]:
                            enc_2d = (enc[0], enc[1])
                            if enc_2d in path:
                                continue
                                
                            for i in range(1, len(path)):
                                # Create a new path with this enclosure inserted
                                new_path = path[:i] + [enc_2d] + path[i:]
                                new_score, new_distance, new_fed = evaluate_path(new_path, zoo_data, fed_enclosures)
                                
                                if new_distance <= battery_capacity and new_score > best_insertion_score:
                                    best_insertion = (i, enc_2d, new_score, new_distance, new_fed)
                                    best_insertion_score = new_score
                        
                        if best_insertion:
                            i, enc_2d, new_score, new_distance, new_fed = best_insertion
                            path = path[:i] + [enc_2d] + path[i:]
                            score = new_score
                            distance = new_distance
                            newly_fed = new_fed
                            improved = True
                    
                    if score > best_score:
                        best_run = path
                        best_score = score
                        best_fed = newly_fed
        
        if best_run:
            drone_runs.append(best_run)
            fed_enclosures.update(best_fed)
        else:
            # No more profitable runs possible
            break
    
    return drone_runs

def optimize_route(points, zoo_data):
    """Optimize the route using 2-opt TSP heuristic"""
    if len(points) <= 3:  # Depot, storage, maybe one enclosure
        return points
    
    # Keep depot as first and last point
    depot = points[0]
    middle_points = points[1:-1]
    
    # Start with a greedy nearest neighbor solution
    current = middle_points[0]
    route = [current]
    unvisited = set(middle_points[1:])
    
    while unvisited:
        nearest = min(unvisited, key=lambda p: distance_2d(current, p))
        route.append(nearest)
        current = nearest
        unvisited.remove(nearest)
    
    # 2-opt improvement
    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 2):
            for j in range(i + 2, len(route)):
                # Calculate current distance
                d1 = distance_2d(route[i], route[i+1])
                d2 = distance_2d(route[j], route[(j+1) % len(route)])
                
                # Calculate new distance if we swap
                d3 = distance_2d(route[i], route[j])
                d4 = distance_2d(route[i+1], route[(j+1) % len(route)])
                
                if d1 + d2 > d3 + d4:
                    # Reverse the route segment
                    route[i+1:j+1] = reversed(route[i+1:j+1])
                    improved = True
    
    # Check for deadzone collisions
    final_route = [depot] + route + [depot]
    for i in range(len(final_route) - 1):
        if intersects_deadzone(final_route[i], final_route[i+1], zoo_data['deadzones']):
            # If there's a collision, revert to simple order
            return points
    
    return final_route
def format_output(runs):
    """Format the drone runs according to the required output format"""
    return str(runs).replace(' ', '')

def solve_megazoo(filename, output_file):
    # Parse zoo configuration
    zoo_data = parse_zoo_file(filename)
    
    # Determine number of battery swaps based on the level
    level_size = max(zoo_data['dimensions'][0], zoo_data['dimensions'][1])
    if level_size <= 100:  # Level 1
        battery_swaps = 1
    elif level_size <= 250:  # Level 2
        battery_swaps = 10
    elif level_size <= 700:  # Level 3
        battery_swaps = 50
    else:  # Level 4
        battery_swaps = 250
    
    # Generate drone runs
    runs = generate_drone_runs(zoo_data, battery_swaps)
    
    # For larger levels, apply TSP optimization
    if level_size > 250:
        optimized_runs = []
        for run in runs:
            optimized_run = optimize_route(run, zoo_data)
            optimized_runs.append(optimized_run)
        runs = optimized_runs
    
    # Format and save output
    with open(output_file, 'w') as file:
        file.write(format_output(runs))
    
    print(f"Solution saved to {output_file}")
    
    # Calculate and print estimated score
    total_score = 0
    total_fed = set()
    for run in runs:
        score, distance, fed = evaluate_path(run, zoo_data, total_fed)
        total_fed.update(fed)
        total_score += score
    
    print(f"Estimated total score: {total_score}")
    print(f"Total enclosures fed: {len(total_fed)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file>")
        sys.exit(1)
    
    solve_megazoo(sys.argv[1], sys.argv[2])