from llm import generate_driver_instructions

route = [
    "Hospital Ministro Costa Cavalcante",
    "Farmácia Cataratas",
    "Droga Raia"
]

print(generate_driver_instructions(route))