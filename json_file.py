import json

def create_level1_json():
    # Define data for level1
    level1_data = {
        "Zoo Dimensions": [100, 100, 50],
        "Drone Depot": [[50, 49, 19]],
        "Battery Distance Capacity": 999999,
        "Food Storages": [
            {"coordinates": [56, 74, 13], "diet": "h"},
            {"coordinates": [38, 79, 11], "diet": "c"},
            {"coordinates": [20, 49, 37], "diet": "o"}
        ],
        "Enclosures": [
            {"coordinates": [7, 12, 7], "importance": 1, "diet": "Carnivore"},
            {"coordinates": [10, 26, 6], "importance": 3, "diet": "Omnivore"}
        ],
        "Deadzones": [],
        "Battery Swaps": 0
    }

    # Write the level1 data to a JSON file
    with open("level1.json", 'w') as f:
        json.dump(level1_data, f, indent=4)
    
    print("Level 1 JSON file created successfully.")

def create_level2_json():
    # Define data for level2
    level2_data = {
        "Zoo Dimensions": [250, 250, 50],
        "Drone Depot": [[119, 127, 24]],
        "Battery Distance Capacity": 1125,
        "Food Storages": [
            {"coordinates": [101, 68, 1], "diet": "h"},
            {"coordinates": [189, 176, 38], "diet": "h"},
            {"coordinates": [128, 174, 7], "diet": "h"},
            {"coordinates": [79, 194, 11], "diet": "c"},
            {"coordinates": [117, 77, 40], "diet": "c"},
            {"coordinates": [127, 70, 2], "diet": "c"},
            {"coordinates": [155, 195, 36], "diet": "o"},
            {"coordinates": [181, 85, 39], "diet": "o"},
            {"coordinates": [128, 97, 18], "diet": "o"}
        ],
        "Enclosures": [
            {"coordinates": [245, 80, 45], "importance": 4.91, "diet": "o"},
            {"coordinates": [142, 90, 38], "importance": 3, "diet": "c"},
            {"coordinates": [18, 23, 13], "importance": 2.47, "diet": "h"},
            {"coordinates": [212, 84, 14], "importance": 7, "diet": "c"},
            {"coordinates": [59, 169, 29], "importance": 13.04, "diet": "h"},
            {"coordinates": [17, 41, 2], "importance": 20, "diet": "c"},
            {"coordinates": [24, 162, 38], "importance": 0.02, "diet": "h"},
            {"coordinates": [6, 93, 45], "importance": 9.23, "diet": "o"},
            {"coordinates": [177, 172, 46], "importance": 23.89, "diet": "h"},
            {"coordinates": [120, 158, 1], "importance": 21, "diet": "c"},
            {"coordinates": [21, 199, 12], "importance": 0.29, "diet": "h"},
            {"coordinates": [0, 31, 30], "importance": 0, "diet": "c"},
            {"coordinates": [212, 4, 10], "importance": 17, "diet": "c"},
            {"coordinates": [54, 101, 26], "importance": 0.02, "diet": "o"},
            {"coordinates": [202, 95, 19], "importance": 2.35, "diet": "o"},
            {"coordinates": [119, 100, 25], "importance": 3, "diet": "c"},
            {"coordinates": [11, 144, 29], "importance": 2, "diet": "c"},
            {"coordinates": [111, 179, 38], "importance": 1.28, "diet": "h"},
            {"coordinates": [114, 232, 3], "importance": 5.02, "diet": "o"},
            {"coordinates": [29, 230, 6], "importance": 2.78, "diet": "h"},
            {"coordinates": [4, 204, 7], "importance": 7.49, "diet": "o"},
            {"coordinates": [109, 226, 48], "importance": 3, "diet": "c"},
            {"coordinates": [198, 118, 28], "importance": 0.33, "diet": "h"},
            {"coordinates": [35, 43, 33], "importance": 16, "diet": "c"},
            {"coordinates": [162, 91, 30], "importance": 0, "diet": "c"},
            {"coordinates": [132, 121, 1], "importance": 5, "diet": "c"},
            {"coordinates": [107, 234, 24], "importance": 5, "diet": "c"},
            {"coordinates": [169, 146, 46], "importance": 3.7, "diet": "o"},
            {"coordinates": [152, 114, 29], "importance": 1.41, "diet": "o"}
        ],
        "Deadzones": [],
        "Battery Swaps": 0
    }

    # Write the level2 data to a JSON file
    with open("level2.json", 'w') as f:
        json.dump(level2_data, f, indent=4)
    
    print("Level 2 JSON file created successfully.")

if __name__ == "__main__":
    # Create level1 and level2 JSON files
    create_level1_json()
    create_level2_json()
