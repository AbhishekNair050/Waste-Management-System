"""Inputs: 
2
varun
borivali
-32 32
both
120
10
o
r
srajan
chembur
25 -12
dry
90
rn
"""

"""
Segregate waste into wet and dry waste,
into organic(o) and inorganic(i) waste, and into recyclable(r) and non-recyclable(n) waste.
Code below Contains Commented Fragments of this on Line 73 87 88 89 90 96 98 99 104 105 106 115 230 231 232 233
"""

import json
import math


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def write(x):
    filename = r'D:\SRAJAN\Python\PP Sem-2 WMS Project\data.json'
    with open(filename, "r+") as file:
        data = json.load(file)
        data.append(x)
        file.seek(0)
        json.dump(data, file)


def get_keys(dictionary):
    result = []
    for key, value in dictionary.items():
        if type(value) is dict:
            new_keys = get_keys(value)
            result.append(key)
            for innerkey in new_keys:
                result.append(innerkey)
        else:
            result.append(key)
    return result


global coords_dict, truck_capacity, trucks  # global variables defined at module level


def main():
    global coords_dict, truck_capacity, trucks  # referencing global variables
    coords_dict = {}
    trucks = 5
    truck_capacity = 100  # KG of waste

    num_houses = int(input("Enter the number of houses: "))

    waste_data = []
    # waste_dict = {'o': 0, 'i': 0, 'r': 0, 'n': 0}
    for i in range(num_houses):
        name = input(f"Enter the name of the person in house {i + 1}: ").title()
        area = input(
            "Enter the area where you reside (Borivali, Chembur, Virar, Goregaon, Mansarovar): ").title()
        coords = tuple(map(int, input("Enter Coordinates (x y): ").split()))
        coords_dict[area] = coords
        waste_type = input("Enter the type of waste (Dry, Wet or Both): ")

        if waste_type.lower() == "both":
            wet_waste = int(
                input(f"Enter the quantity of wet waste for house {i + 1}: "))
            dry_waste = int(
                input(f"Enter the quantity of dry waste for house {i + 1}: "))
            # WetWaste = input("Enter wet waste: ")  # oi
            # DryWaste = input("Enter dry waste: ")  # rn
            # for i in WetWaste + DryWaste:
            #     waste_dict[i] += WetWaste.count(i) + DryWaste.count(i)


        elif waste_type.lower() == "wet":
            wet_waste = int(
                input(f"Enter the quantity of wet waste for house {i + 1}: "))
            # WetWaste = input("Enter wet waste: ")
            dry_waste = 0
            # for i in WetWaste:
            #     waste_dict[i] += WetWaste.count(i)
        else:
            wet_waste = 0
            dry_waste = int(
                input(f"Enter the quantity of dry waste for house {i + 1}: "))
            # DryWaste = input("Enter dry waste: ")
            # for i in DryWaste:
            #     waste_dict[i] += DryWaste.count(i)

        waste_data.append({
            "Name": name,
            "Area": area,
            "Waste Type": waste_type,
            "Wet Waste": wet_waste,
            "Dry Waste": dry_waste
        })
    # print(waste_dict)
    write(waste_data)

    total_wet_waste = sum([row["Wet Waste"] for row in waste_data])
    total_dry_waste = sum([row["Dry Waste"] for row in waste_data])

    total_waste = total_wet_waste + total_dry_waste
    percent_wet_waste = (total_wet_waste / total_waste) * 100
    percent_dry_waste = (total_dry_waste / total_waste) * 100

    print(f"\nTotal wet waste generated: {total_wet_waste} kg")
    print(f"Total dry waste generated: {total_dry_waste} kg")
    print(f"Percentage of wet waste: {percent_wet_waste:.2f}%")
    print(f"Percentage of dry waste: {percent_dry_waste:.2f}%")

    waste_per_house = []

    for row in waste_data:
        total_waste = row["Wet Waste"] + row["Dry Waste"]
        waste_per_house.append((row["Name"], total_waste))
    print("\nTotal waste generated per house:")
    for house in waste_per_house:
        print(f"{house[0]}: {house[1]} kg")

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

    sorted_areas = {k: v for k, v in sorted(
        area_waste.items(), key=lambda x: x[1], reverse=True)}
    sort_just_areas = [k for k, v in sorted_areas.items()]
    print(f"Priority area based on waste generation: {sort_just_areas[0]}")

    effi_dist_loc = []
    for j in range(1, len(sort_just_areas)):
        x2_x1 = [(coords_dict[sort_just_areas[i]][0] - coords_dict[sort_just_areas[0]][0])
                 ** 2 for i in range(1, len(sort_just_areas)) if i != 0]
        y2_y1 = [(coords_dict[sort_just_areas[i]][1] - coords_dict[sort_just_areas[0]][1])
                 ** 2 for i in range(1, len(sort_just_areas)) if i != 0]
        x2x1_y2y1 = [abs(x2_x1[i] + y2_y1[i]) for i in range(len(x2_x1))]
        dist_priority = {sort_just_areas[0]: {sort_just_areas[i]: (
                abs(x2x1_y2y1[i - 1]) ** 0.5) for i in range(1, len(sort_just_areas)) if i != 0}}

        dist_priority_key = get_keys(dist_priority)

        effi_dist_loc.append(dist_priority_key[0])
        dist_priority_key.remove(dist_priority_key[0])
        sort_just_areas = dist_priority_key

    effi_dist_loc.append(sort_just_areas[0])

    print(f"{Color.BOLD}MOST EFFICIENT ROUTE:{Color.END}")
    print(effi_dist_loc)
    for i in range(len(effi_dist_loc)):
        print(f"{i + 1}. {Color.ITALIC}{effi_dist_loc[i]}{Color.END}")

    waste_left = {i: sorted_areas[i] for i in effi_dist_loc if i in sorted_areas}

    print(f"\nWaste per Area on route, {waste_left}")
    print('')
    total_waste = sum(v for k, v in sorted_areas.items())

    waste_carried = [0] * trucks

    truck_index = 0

    for loc in effi_dist_loc:

        num_trucks_loc = math.ceil(waste_left[loc] / truck_capacity)

        for i in range(num_trucks_loc):

            if truck_capacity == waste_carried[truck_index]:
                truck_index = (truck_index + 1) % trucks
                waste_carried[truck_index] = 0

            space_left = truck_capacity - waste_carried[truck_index]

            if space_left < waste_left[loc]:
                waste_collected = space_left
                waste_left[loc] -= space_left
            else:
                waste_collected = waste_left[loc]
                waste_left[loc] = 0

            waste_carried[truck_index] += waste_collected
            print(
                f"Sending truck {truck_index + 1} to {loc}, waste collected: {waste_collected:.2f} kg")

            if all(w == 100 for w in waste_carried):
                print(
                    f"All trucks used.")
                break
            if waste_left[loc] == 0:
                break
            truck_index = (truck_index + 1) % trucks

        if all(w == 100 for w in waste_carried):
            break
        if waste_left[loc] > 0:
            print(
                f"Sending truck {truck_index + 1} to {loc}, waste collected: {waste_left[loc]:.2f} kg")
            waste_carried[truck_index] += waste_left[loc]
            waste_left[loc] = 0

    num_trucks_used = sum([1 for waste in waste_carried if waste > 0])
    if total_waste == sum(waste_carried) and total_waste - sum(waste_carried) == 0:
        print(f"{Color.BOLD}All waste collected in {num_trucks_used} trucks.{Color.END}")
        # if waste_dict['o'] != 0: print(f"Sending Organic waste, {waste_dict['o']} to Organic waste plant.")
        # if waste_dict['i'] != 0: print(f"Sending Inorganic waste, {waste_dict['i']} to Inorganic waste plant.")
        # if waste_dict['r'] != 0: print(f"Sending Recyclable waste, {waste_dict['r']} to Recyclable waste plant.")
        # if waste_dict['n'] != 0: print(f"Sending Non-Recyclable waste, {waste_dict['n']} for Re-Use.")

    else:
        print(
            f"{Color.BOLD}All waste could not be collected in {num_trucks_used} trucks, {total_waste - sum(waste_carried):.2f} kg waste left.{Color.END}")
        print(
            f"{Color.BOLD}Additional trucks required: {math.ceil((total_waste - sum(waste_carried)) / truck_capacity)}{Color.END}")
        print(f"\nWaste left in each location: {waste_left}")

    #
    """Experimental code for demostrating the most efficient route. Can replace code from line 138 to 159."""
    # import googlemaps
    # from datetime import datetime
    #
    # # Replace YOUR_API_KEY with actual Google Maps API key
    # gmaps = googlemaps.Client(key='YOUR_API_KEY')
    #
    # locations = get_keys(dist_priority)
    # start = locations[0]
    # end = locations[1]
    #
    # stops = [coords_dict[area] for area in locations[1:-1]]
    #
    # now = datetime.now()
    #
    # directions_result = gmaps.directions(
    #     start, end, mode="transit", departure_time=now, waypoints=stops)
    #
    # print(directions_result[0]['summary'])


if __name__ == "__main__":
    main()
