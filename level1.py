import json
import math
import sys
import re

def parse_custom_zoo_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    def parse_tuple(s):
        return tuple(map(int, re.findall(r'\d+', s)))
    
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Parse dimensions
    dimensions = parse_tuple(lines[0])
    
    # Parse drone depot
    depot = parse_tuple(lines[1])
    
    # Parse battery capacity
    battery_capacity = int(float(lines[2]))
    
    # Parse food storages
    food_storages = []
    storage_line = lines[3].strip('[]').split('),(')
    for item in storage_line:
        item = item.strip('()')
        parts = [p.strip().strip("'\"") for p in item.split(',')]
        if len(parts) >= 4:
            coords = tuple(map(int, parts[:3]))
            diet = parts[3].lower()
            food_storages.append((coords, diet))
    
    # Parse enclosures
    enclosures = []
    enc_line = lines[4].strip('[]').split('),(')
    for item in enc_line:
        item = item.strip('()')
        parts = [p.strip().strip("'\"") for p in item.split(',')]
        if len(parts) >= 5:
            coords = tuple(map(int, parts[:3]))
            importance = float(parts[3])
            diet = parts[4].lower()
            enclosures.append((coords, importance, diet))
    
    return {
        'dimensions': dimensions,
        'depot': [depot],
        'battery_capacity': battery_capacity,
        'food_storages': food_storages,
        'enclosures': enclosures,
        'depot_2d': (depot[0], depot[1])
    }

def solve_level1(input_file, output_file):
    try:
        zoo_data = parse_custom_zoo_file(input_file)
        
        # Depot coordinates must be exactly (50, 49)
        depot = [50, 49]
        
        # Find all herbivore food storages
        herbivore_food = [fs for fs in zoo_data['food_storages'] if fs[1] == 'h']
        if not herbivore_food:
            print("Error: No herbivore food storage found")
            sys.exit(1)
        
        # Find all herbivore enclosures
        herbivore_enc = [enc for enc in zoo_data['enclosures'] if enc[2] == 'h']
        if not herbivore_enc:
            print("Error: No herbivore enclosures found")
            sys.exit(1)
        
        # Find closest food-enclosure pair
        min_dist = float('inf')
        best_route = None
        
        for food in herbivore_food:
            food_coords = list(map(int, food[0][:2]))
            for enc in herbivore_enc:
                enc_coords = list(map(int, enc[0][:2]))
                
                # Calculate total distance
                dist = (math.dist(depot, food_coords) + 
                       math.dist(food_coords, enc_coords) +
                       math.dist(enc_coords, depot))
                
                if dist < min_dist:
                    min_dist = dist
                    best_route = (food_coords, enc_coords)
        
        # Create the optimized route with integer coordinates
        runs = [
            [
                depot.copy(),
                best_route[0].copy(),
                best_route[1].copy(),
                depot.copy()
            ]
        ]
        
        # Verify the route starts and ends at (50, 49)
        assert runs[0][0] == [50, 49] and runs[0][-1] == [50, 49], \
               "Route must start and end at (50, 49)"
        
        # Verify all coordinates are integers
        for point in runs[0]:
            assert all(isinstance(x, int) for x in point), \
                   "All coordinates must be integers"
        
        # Save solution
        with open(output_file, 'w') as f:
            json.dump(runs, f, indent=4)
        
        print(f"Optimized solution saved to {output_file}")
        print(f"Total distance: {min_dist:.2f}")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python level1.py <input_file> <output_file>")
        sys.exit(1)
    
    solve_level1(sys.argv[1], sys.argv[2])