import json

# Data structure to represent the JSON for each level
levels_data = {
    "Level 1": {
        "Zoo Dimensions": [100, 100, 50],
        "Drone Depot": [[7, 24, 5], [6, 9, 2]],
        "Battery Distance Capacity": 999999,
        "Food Storages": [
            {"coordinates": [5, 20, 1], "diet": "Omnivore"},
            {"coordinates": [9, 18, 0], "diet": "Herbivore"}
        ],
        "Enclosures": [
            {"coordinates": [7, 12, 7], "importance": 1, "diet": "Carnivore"},
            {"coordinates": [10, 26, 6], "importance": 3, "diet": "Omnivore"}
        ],
        "Deadzones": [],
        "Battery Swaps": 0
    },
    "Level 2": {
        "Zoo Dimensions": [250, 250, 50],
        "Drone Depot": [[5, 5, 12], [8, 10, 10], [8, 4, 6]],
        "Battery Distance Capacity": 1125,
        "Food Storages": [
            {"coordinates": [5, 20, 1], "diet": "Omnivore"},
            {"coordinates": [9, 18, 0], "diet": "Herbivore"}
        ],
        "Enclosures": [
            {"coordinates": [7, 12, 7], "importance": 1, "diet": "Carnivore"},
            {"coordinates": [10, 26, 6], "importance": 3, "diet": "Omnivore"}
        ],
        "Deadzones": [
            {"coordinates": [13, 14, 21], "radius": 3},
            {"coordinates": [12, 8, 5], "radius": 3}
        ],
        "Battery Swaps": 10
    },
    "Level 3": {
        "Zoo Dimensions": [700, 700, 50],
        "Drone Depot": [[7, 24, 5], [6, 9, 2], [7, 12, 7], [8, 10, 10], [5, 5, 12], [8, 4, 6], [10, 26, 6]],
        "Battery Distance Capacity": 2750,
        "Food Storages": [
            {"coordinates": [5, 20, 1], "diet": "Omnivore"},
            {"coordinates": [9, 18, 0], "diet": "Herbivore"}
        ],
        "Enclosures": [
            {"coordinates": [7, 12, 7], "importance": 1, "diet": "Carnivore"},
            {"coordinates": [10, 26, 6], "importance": 3, "diet": "Omnivore"}
        ],
        "Deadzones": [
            {"coordinates": [13, 14, 21], "radius": 3},
            {"coordinates": [12, 8, 5], "radius": 3},
            {"coordinates": [16, 13, 20], "radius": 3}
        ],
        "Battery Swaps": 50
    },
    "Level 4": {
        "Zoo Dimensions": [2500, 2500, 50],
        "Drone Depot": [[7, 24, 5], [6, 9, 2], [7, 12, 7], [8, 10, 10], [5, 5, 12], [8, 4, 6], [10, 26, 6]],
        "Battery Distance Capacity": 9250,
        "Food Storages": [
            {"coordinates": [5, 20, 1], "diet": "Omnivore"},
            {"coordinates": [9, 18, 0], "diet": "Herbivore"},
            {"coordinates": [6, 9, 2], "diet": "Carnivore"}
        ],
        "Enclosures": [
            {"coordinates": [7, 12, 7], "importance": 1, "diet": "Carnivore"},
            {"coordinates": [10, 26, 6], "importance": 3, "diet": "Omnivore"}
        ],
        "Deadzones": [
            {"coordinates": [13, 14, 21], "radius": 3},
            {"coordinates": [12, 8, 5], "radius": 3},
            {"coordinates": [16, 13, 20], "radius": 3},
            {"coordinates": [14, 18, 7], "radius": 3},
            {"coordinates": [19, 20, 4], "radius": 3}
        ],
        "Battery Swaps": 250
    }
}

# Save as .json files instead of .txt for better clarity
file_names = ["level1.json", "level2.json", "level3.json", "level4.json"]
for i, level in enumerate(levels_data.values()):
    with open(file_names[i], 'w') as file:
        json.dump(level, file, indent=4)

print("Files created:", file_names)
