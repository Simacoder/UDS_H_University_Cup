import json

def parse_zoo_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    return {
        'dimensions': tuple(data["Zoo Dimensions"]),
        'drone_depot': [tuple(dep) for dep in data["Drone Depot"]],
        'battery_capacity': data["Battery Distance Capacity"],
        'food_storages': [(tuple(fs["coordinates"]), fs["diet"]) for fs in data["Food Storages"]],
        'enclosures': [(tuple(enc["coordinates"]), enc["importance"], enc["diet"]) for enc in data["Enclosures"]],
        'deadzones': [(tuple(dz["coordinates"]), dz["radius"]) for dz in data.get("Deadzones", [])],
        'battery_swaps': data.get("Battery Swaps", 0),
        'depot_2d': tuple(data["Drone Depot"][0][:2])  # 👈 Add this line
    }

def calculate_distance(point1, point2, flight_height=50):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    vertical_distance = abs(flight_height - z1) + abs(flight_height - z2)
    horizontal_distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return vertical_distance + horizontal_distance

def distance_2d(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def intersects_deadzone(p1, p2, deadzones):
    x1, y1 = p1
    x2, y2 = p2
    for (x, y, _), r in deadzones:
        dx, dy = x - x1, y - y1
        line_len = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        if line_len == 0:
            return distance_2d((x1, y1), (x, y)) <= r
        udx, udy = (x2 - x1) / line_len, (y2 - y1) / line_len
        t = max(0, min(line_len, dx * udx + dy * udy))
        px, py = x1 + t * udx, y1 + t * udy
        closest_dist = ((px - x)**2 + (py - y)**2)**0.5
        if closest_dist <= r:
            return True
    return False

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
    
    # Convert to 3D by adding the flight height (50)
    food_storage_coords_3d = food_storage_coords + (50,)
    
    # Now calculate the distance with 3D points
    distance = calculate_distance(depot_3d, food_storage_coords_3d)
    print(f"Distance from depot to food storage: {distance}")
    
    # Example: Check if the path from the depot to the food storage intersects with any deadzone
    deadzones = zoo_data['deadzones']
    intersects = intersects_deadzone(depot_2d, food_storage_coords, deadzones)
    print(f"Path intersects deadzone: {intersects}")

if __name__ == "__main__":
    main()
