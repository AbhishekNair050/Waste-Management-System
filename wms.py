# import json

# num_houses = int(input("Enter the number of houses: "))
# recycle = input("Are you willing to recycle waste? (Yes/No): ")
# waste_data = []

# for i in range(num_houses):
#     name = input("Enter the name of the person in house {}: ".format(i+1))
#     flat_num = input(
#         "Enter the flat number of the person in house {}: ".format(i+1))

#     wet_waste = input(
#         "Enter the quantity of wet waste for house {}: ".format(i+1))
#     dry_waste = input(
#         "Enter the quantity of dry waste for house {}: ".format(i+1))

#     waste_data.append({"Name": name, "Flat Number": flat_num,
#                       "Wet Waste": wet_waste, "Dry Waste": dry_waste})

# with open('waste_data.json', 'w') as file:
#     json.dump(waste_data, file)

# with open('waste_data.json', 'r') as file:
#     data = json.load(file)

# total_wet_waste = sum([int(row["Wet Waste"]) for row in data])
# total_dry_waste = sum([int(row["Dry Waste"]) for row in data])

# total_waste = total_wet_waste + total_dry_waste
# percent_wet_waste = (total_wet_waste / total_waste) * 100
# percent_dry_waste = (total_dry_waste / total_waste) * 100

# print("Total wet waste generated: {} kg".format(total_wet_waste))
# print("Total dry waste generated: {} kg".format(total_dry_waste))
# print("Percentage of wet waste: {:.2f}%".format(percent_wet_waste))
# print("Percentage of dry waste: {:.2f}%".format(percent_dry_waste))

# waste_per_house = []
# for row in data:
#     total_waste = int(row["Wet Waste"]) + int(row["Dry Waste"])
#     waste_per_house.append((row["Name"], row["Flat Number"], total_waste))

# print("\nTotal waste generated per house:")
# for house in waste_per_house:
#     print("Flat Number {}: {} kg".format(house[1], house[2]))


import heapq
import json

num_houses = int(input("Enter the number of houses: "))

waste_data = []

for i in range(num_houses):
    name = input("Enter the name of the person in house {}: ".format(i+1))
    area = input(
        "Enter the area where you reside (Borivali, Chembur, Virar, Goregaon, Mansarovar): ")
    waste_type = input("Enter the type of waste (Dry, Wet or Both): ")

    if waste_type.lower() == "both":
        wet_waste = int(
            input("Enter the quantity of wet waste for house {}: ".format(i+1)))
        dry_waste = int(
            input("Enter the quantity of dry waste for house {}: ".format(i+1)))
    elif waste_type.lower() == "wet":
        wet_waste = int(
            input("Enter the quantity of wet waste for house {}: ".format(i+1)))
        dry_waste = 0
    else:
        wet_waste = 0
        dry_waste = int(
            input("Enter the quantity of dry waste for house {}: ".format(i+1)))

    waste_data.append({
        "Name": name,
        "Area": area,
        "Waste Type": waste_type,
        "Wet Waste": wet_waste,
        "Dry Waste": dry_waste
    })

with open('waste_data.json', 'w') as file:
    json.dump(waste_data, file)

with open('waste_data.json', 'r') as file:
    data = json.load(file)

total_wet_waste = sum([row["Wet Waste"] for row in data])
total_dry_waste = sum([row["Dry Waste"] for row in data])

total_waste = total_wet_waste + total_dry_waste
percent_wet_waste = (total_wet_waste / total_waste) * 100
percent_dry_waste = (total_dry_waste / total_waste) * 100

print("Total wet waste generated: {} kg".format(total_wet_waste))
print("Total dry waste generated: {} kg".format(total_dry_waste))
print("Percentage of wet waste: {:.2f}%".format(percent_wet_waste))
print("Percentage of dry waste: {:.2f}%".format(percent_dry_waste))

waste_per_house = []
for row in data:
    total_waste = row["Wet Waste"] + row["Dry Waste"]
    waste_per_house.append((row["Name"], total_waste))
print("\nTotal waste generated per house:")
for house in waste_per_house:
    print("{}: {} kg".format(house[0], house[1]))

area_waste = {}
for data in waste_data:
    area = data["Area"]
    wet_waste = data["Wet Waste"]
    dry_waste = data["Dry Waste"]
    total_waste = wet_waste + dry_waste
    if area not in area_waste:
        area_waste[area] = total_waste
    else:
        area_waste[area] += total_waste

sorted_areas = sorted(area_waste.items(), key=lambda x: x[1], reverse=True)
print("Priority area based on waste generation:")
print(sorted_areas[0][0])
print(sorted_areas)


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    visited = set()
    while heap:
        (current_distance, current_node) = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))
    return distances


# create a weighted graph
graph = {
    "Borivali": {"Chembur": 25, "Virar": 50, "Goregaon": 15, "Mansarovar": 30},
    "Chembur": {"Borivali": 25, "Virar": 55, "Goregaon": 40, "Mansarovar": 30},
    "Virar": {"Borivali": 50, "Chembur": 55, "Goregaon": 45, "Mansarovar": 35},
    "Goregaon": {"Borivali": 15, "Chembur": 40, "Virar": 45, "Mansarovar": 20},
    "Mansarovar": {"Borivali": 30, "Chembur": 30, "Virar": 35, "Goregaon": 20}
}

# add weights based on waste generation
for area_name, waste_amount in area_waste.items():
    if area_name != sorted_areas[0][0]:
        weight = 10000 - waste_amount
        for neighbor in graph[area_name]:
            graph[area_name][neighbor] += weight
            graph[neighbor][area_name] += weight

# find the shortest route starting from the priority area
distances = dijkstra(graph, sorted_areas[0][0])
sorted_distances = sorted(distances.items(), key=lambda x: x[1])
route = [sorted_areas[0][0]]
truck_load = 0
for i in range(1, len(sorted_distances)):
    area_name = sorted_distances[i][0]
    distance = sorted_distances[i][1]
    if area_name != sorted_areas[0][0] and truck_load + area_waste[area_name] <= 300:
        route.append(area_name)
        truck_load += area_waste[area_name]
    else:
        break

print("Shortest route while keeping the priority list in mind:")
print(" -> ".join(route))