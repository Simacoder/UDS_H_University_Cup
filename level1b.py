import json
import sys
from megazoo_utils import parse_zoo_file

def solve_level1(input_file, output_file):
    # Parse the input zoo data
    zoo_data = parse_zoo_file(input_file)

    # Get the 2D (x, y) coordinates of the drone depot
    depot = zoo_data['depot_2d']  # Should be something like (50, 49)

    # Get the 2D coordinate of the first food storage location
    food_storage_3d, _ = zoo_data['food_storages'][0]
    food_storage = (food_storage_3d[0], food_storage_3d[1])  # Convert to 2D (x, y)

    # Create the drone run: depot -> food storage -> depot
    run = [depot, food_storage, depot]
    runs = [run]

    # Save the result to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(runs, f, indent=4)

    print(f"Level 1 solution saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python level1.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    solve_level1(input_path, output_path)
