import json
from megazoo_utils import parse_zoo_file
import sys

def solve_level2(input_file, output_file):
    # Parse the zoo data from the input file
    zoo_data = parse_zoo_file(input_file)
    
    # Get the actual coordinates of the drone depot
    depot = zoo_data['depot_2d']
    print(f"Depot coordinates: {depot}")
    
    # Get the first food storage coordinates (assuming food storage contains tuples of coordinates and diet)
    storage = zoo_data['food_storages'][0][0]  # Get the 2D coordinates
    print(f"Food storage coordinates: {storage}")
    
    # Get the first enclosure coordinates (assuming enclosures contain coordinates and diet)
    enclosure = zoo_data['enclosures'][0][0]  # Get the 2D coordinates
    print(f"Enclosure coordinates: {enclosure}")
    
    # Create the run sequence from depot -> storage -> enclosure -> depot
    runs = [[depot, storage, enclosure, depot]]
    print(f"Drone run path: {runs}")
    
    # Write the solution to the output file in JSON format
    with open(output_file, 'w') as f:
        json.dump(runs, f, indent=4)
    
    print(f"Level 2 solution saved to {output_file}")

if __name__ == "__main__":
    # Ensure correct command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python level2.py <input_file> <output_file>")
        sys.exit(1)
    
    solve_level2(sys.argv[1], sys.argv[2])
