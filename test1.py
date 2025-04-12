import json
from megazoo_utils import parse_zoo_file, calculate_distance, intersects_deadzone

def main():
    # Parse the zoo data from the input file
    zoo_data = parse_zoo_file("level1.json")
    
    # Get the drone depot's 2D coordinates
    depot_2d = zoo_data['depot_2d']
    print(f"Drone Depot 2D Coordinates: {depot_2d}")
    
    # Convert to 3D by adding the flight height (50)
    depot_3d = depot_2d + (50,)
    
    # Example: Calculate the distance from the depot to a food storage
    food_storage_coords = zoo_data['food_storages'][0][0]  # First food storage's coordinates
    print(f"Food Storage Coordinates: {food_storage_coords}")
    
    # Now calculate the distance with 3D points
    distance = calculate_distance(depot_3d, food_storage_coords)
    print(f"Distance from depot to food storage: {distance}")
    
    # Example: Check if the path from the depot to the food storage intersects with any deadzone
    # Use only the 2D coordinates for the intersection check
    deadzones = zoo_data['deadzones']
    intersects = intersects_deadzone(depot_2d, food_storage_coords[:2], deadzones)  # Pass only 2D coordinates
    print(f"Path intersects deadzone: {intersects}")

if __name__ == "__main__":
    main()
