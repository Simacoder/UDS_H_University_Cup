# level3.py

from megazoo_utils import parse_zoo_file
# Reuse the logic from level2
from level4 import evaluate_path, generate_drone_runs  # Reuse the logic from level4
import sys

def solve_level3(input_file, output_file):
    zoo_data = parse_zoo_file(input_file)
    runs = generate_drone_runs(zoo_data, battery_swaps=50)
    
    with open(output_file, 'w') as f:
        f.write(str(runs).replace(" ", ""))
    
    print(f"Level 3 solution saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python level3.py <input_file> <output_file>")
        sys.exit(1)
    
    solve_level3(sys.argv[1], sys.argv[2])
