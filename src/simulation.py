#Keeps all logistics rules.
from math import ceil

def split_route_among_vehicles(route, number_of_vehicles):
    """
    Split one optimized route into several vehicle routes.
    """

    chunk_size = ceil(len(route) / number_of_vehicles)

    vehicle_routes = []

    for i in range(number_of_vehicles):

        start = i * chunk_size
        end = start + chunk_size

        vehicle_routes.append(route[start:end])

    return vehicle_routes

def print_vehicle_summary(vehicle_routes):

    print("\n========== VEHICLE ROUTES ==========\n")

    for i, route in enumerate(vehicle_routes):

        print(f"Vehicle {i+1}")

        print(f"Stops: {len(route)}")

        print("------------------------")