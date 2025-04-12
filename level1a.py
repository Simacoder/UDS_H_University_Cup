import json
import math
import sys
from typing import List, Tuple

def parse_zoo_file(filename: str) -> dict:
    """Parse the zoo data file into a structured dictionary."""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    return {
        'dimensions': tuple(data["Zoo Dimensions"]),
        'depot': tuple(data["Drone Depot"][0][:2]),  # (x, y) only
        'battery': data["Battery Distance Capacity"],
        'food_storages': [(tuple(fs["coordinates"]), fs["diet"]) for fs in data["Food Storages"]],
        'enclosures': [(tuple(enc["coordinates"]), enc["importance"], enc["diet"]) for enc in data["Enclosures"]],
        'deadzones': [(tuple(dz["coordinates"]), dz["radius"]) for dz in data.get("Deadzones", [])]
    }

def find_optimal_route(zoo_data: dict) -> List[List[int]]:
    """Find the most efficient route that starts/ends at depot and visits herbivore locations."""
    depot = [50, 49]  # Must be exactly this coordinate
    
    # Find all herbivore food sources
    h_foods = [fs for fs in zoo_data['food_storages'] if fs[1].lower() == 'h']
    if not h_foods:
        raise ValueError("No herbivore food sources found")
    
    # Find all herbivore enclosures
    h_enclosures = [enc for enc in zoo_data['enclosures'] if enc[2].lower() == 'herbivore']
    if not h_enclosures:
        raise ValueError("No herbivore enclosures found")
    
    # Find the closest food-enclosure pair
    min_distance = float('inf')
    best_path = None
    
    for food in h_foods:
        food_xy = list(map(int, food[0][:2]))
        for enc in h_enclosures:
            enc_xy = list(map(int, enc[0][:2]))
            
            # Calculate total distance
            dist = (math.dist(depot, food_xy) + 
                   math.dist(food_xy, enc_xy) + 
                   math.dist(enc_xy, depot))
            
            if dist < min_distance:
                min_distance = dist
                best_path = [depot.copy(), food_xy, enc_xy, depot.copy()]
    
    return [best_path] if best_path else None

def validate_route(route: List[List[int]]) -> None:
    """Ensure the route meets all requirements."""
    if not route:
        raise ValueError("No valid route found")
    
    # Check start/end at (50, 49)
    if route[0][0] != [50, 49] or route[0][-1] != [50, 49]:
        raise ValueError("Route must start and end at (50, 49)")
    
    # Check all coordinates are integers
    for point in route[0]:
        if not all(isinstance(x, int) for x in point):
            raise ValueError("All coordinates must be integers")

def solve_level1(input_file: str, output_file: str) -> None:
    """Main solution function for Level 1."""
    try:
        # Parse input data
        zoo_data = parse_zoo_file(input_file)
        
        # Calculate optimal route
        route = find_optimal_route(zoo_data)
        if not route:
            print("No valid route could be calculated")
            sys.exit(1)
        
        # Validate the route
        validate_route(route)
        
        # Save the solution
        with open(output_file, 'w') as f:
            json.dump(route, f, indent=4)
        
        print(f"Success! Solution saved to {output_file}")
        print(f"Route: {route}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python level1.py <input_file> <output_file>")
        sys.exit(1)
    
    solve_level1(sys.argv[1], sys.argv[2])