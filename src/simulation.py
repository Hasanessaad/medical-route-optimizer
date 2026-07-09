#Keeps all logistics rules.
from math import ceil

def split_route_among_vehicles(
    route,
    number_of_vehicles,
    location_lookup
):
    """
    Split one optimized route while balancing
    package weight between vehicles.
    """

    vehicle_routes = [
        []
        for _ in range(number_of_vehicles)
    ]

    vehicle_weights = [
        0
        for _ in range(number_of_vehicles)
    ]

    for city_id in route:

        location = location_lookup[city_id]

        weight = location["package_weight"]

        smallest_vehicle = vehicle_weights.index(
            min(vehicle_weights)
        )

        vehicle_routes[smallest_vehicle].append(city_id)

        vehicle_weights[smallest_vehicle] += weight

    return vehicle_routes

def print_vehicle_summary(
    vehicle_routes,
    location_lookup
):

    print("\n========== VEHICLE ROUTES ==========\n")

    for i, route in enumerate(vehicle_routes):

        total_weight = sum(
            location_lookup[city]["package_weight"]
            for city in route
        )

        print(f"Vehicle {i+1}")
        print(f"Stops : {len(route)}")
        print(f"Weight: {total_weight} kg")
        print("------------------------")