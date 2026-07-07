#Handles the LLM integration.
from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_driver_instructions(route, location_lookup):

    route_description = []

    for i, city_id in enumerate(route):

        location = location_lookup[city_id]

        route_description.append(
            f"""
Stop {i+1}

Location: {location['name']}
Type: {location['type']}
Priority: {location['priority']}
Delivery: {location['delivery_type']}
Weight: {location['package_weight']} kg
"""
        )

    prompt = f"""
You are an experienced medical logistics assistant.

Generate detailed instructions for a delivery driver.

Optimized Route:

{''.join(route_description)}

Include:

- Route summary
- First stop
- High priority deliveries
- Delivery recommendations
- Safety observations
- Estimated workload

Write professionally.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception:

            time.sleep(2)

    return "Unable to generate driver instructions because the LLM service is temporarily unavailable."

def explain_vehicle_route(route, location_lookup):

    explanation = []

    explanation.append(
        f"The vehicle will visit {len(route)} healthcare locations."
    )

    high_priority = 0

    hospitals = 0

    pharmacies = 0

    total_weight = 0

    for city_id in route:

        location = location_lookup[city_id]

        total_weight += location["package_weight"]

        if location["priority"] == 3:
            high_priority += 1

        if location["type"] == "hospital":
            hospitals += 1

        if location["type"] == "pharmacy":
            pharmacies += 1

    explanation.append(
        f"High-priority deliveries: {high_priority}"
    )

    explanation.append(
        f"Hospitals: {hospitals}"
    )

    explanation.append(
        f"Pharmacies: {pharmacies}"
    )

    explanation.append(
        f"Estimated package weight: {total_weight} kg"
    )

    return "\n".join(explanation)

def generate_daily_report(
    best_fitness,
    vehicle_routes,
    location_lookup
):

    total_deliveries = 0
    total_priority = 0
    total_weight = 0
    total_hospitals = 0
    total_pharmacies = 0

    for route in vehicle_routes:

        total_deliveries += len(route)

        for city_id in route:

            location = location_lookup[city_id]

            total_weight += location["package_weight"]

            if location["priority"] == 3:
                total_priority += 1

            if location["type"] == "hospital":
                total_hospitals += 1

            if location["type"] == "pharmacy":
                total_pharmacies += 1

    prompt = f"""
        You are a logistics manager.

        Create a professional daily report.

        Today's statistics:

        Total deliveries: {total_deliveries}

        Vehicles used: {len(vehicle_routes)}

        Hospitals served: {total_hospitals}

        Pharmacies served: {total_pharmacies}

        High priority deliveries: {total_priority}

        Estimated transported weight: {total_weight} kg

        Best fitness score: {best_fitness:.2f}

        Write a professional report including:

        - operational summary
        - route efficiency
        - possible bottlenecks
        - recommendations
        """

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception:

            time.sleep(2)

    return "Unable to generate the daily report because the LLM service is temporarily unavailable."

def ask_question(question, vehicle_routes, location_lookup):

    summary = []

    for i, route in enumerate(vehicle_routes):

        high_priority = 0
        hospitals = 0
        pharmacies = 0
        weight = 0

        for city_id in route:

            location = location_lookup[city_id]

            weight += location["package_weight"]

            if location["priority"] == 3:
                high_priority += 1

            if location["type"] == "hospital":
                hospitals += 1

            if location["type"] == "pharmacy":
                pharmacies += 1

        summary.append(
            f"""
Vehicle {i+1}

Stops: {len(route)}

High priority deliveries: {high_priority}

Hospitals: {hospitals}

Pharmacies: {pharmacies}

Package weight: {weight} kg
"""
        )

    prompt = f"""
You are a medical logistics assistant.

Answer ONLY using the information below.

Vehicle statistics:

{''.join(summary)}

Question:

{question}

If the answer cannot be determined from the statistics, say so.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception:

            time.sleep(2)

    return "Unable to answer the question because the LLM service is temporarily unavailable."