# Medical Route Optimization using Genetic Algorithms and Large Language Models

## Overview

This project was developed as part of the FIAP Tech Challenge for the Medical AI module.

The objective is to optimize the distribution of medications and medical supplies between healthcare facilities using a **Genetic Algorithm (GA)** while integrating a **Large Language Model (LLM)** to automatically generate driver instructions, operational reports, and answer logistics-related questions.

The project extends a basic Travelling Salesman Problem (TSP) implementation by incorporating realistic healthcare logistics constraints, making the optimization process closer to real-world medical distribution scenarios.

---

# Features

- Genetic Algorithm for route optimization
- Real healthcare dataset (90 locations)
- Delivery priority optimization
- Vehicle capacity constraints
- Vehicle autonomy (maximum route distance)
- Multi-vehicle route distribution (VRP extension)
- Route visualization using Pygame
- Tournament Selection
- Order Crossover (OX)
- Swap Mutation
- Elitism
- AI-generated driver instructions
- AI-generated logistics reports
- Natural language route analysis using Gemini

---

# Technologies

- Python 3.12
- Pygame
- NumPy
- Pandas
- Google Gemini API
- Python Dotenv
- Git & GitHub

---

# Project Structure

```
medical-route-optimizer/

│
├── data/
│   └── foz_healthcare_locations.csv
│
├── src/
│   ├── tsp.py
│   ├── genetic_algorithm.py
│   ├── data_loader.py
│   ├── draw_functions.py
│   ├── simulation.py
│   ├── llm.py
│   ├── benchmark_att48.py
│   └── test_llm.py
│
├── outputs/
│   ├── reports/
│   └── driver_instructions/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# How the System Works

```
Healthcare Dataset
        │
        ▼
Load Healthcare Locations
        │
        ▼
Normalize GPS Coordinates
        │
        ▼
Generate Initial Population
        │
        ▼
Genetic Algorithm
        │
        ├── Selection
        ├── Crossover
        ├── Mutation
        ├── Fitness Evaluation
        └── Elitism
        │
        ▼
Best Optimized Route
        │
        ▼
Split Route Among Vehicles
        │
        ▼
Vehicle Analysis
        │
        ▼
Gemini AI
        ├── Driver Instructions
        ├── Daily Report
        └── Question Answering
```

---

# Genetic Algorithm

Each chromosome represents an ordered sequence of healthcare locations.

The Genetic Algorithm follows the classical evolutionary cycle:

1. Generate initial population
2. Evaluate fitness
3. Tournament selection
4. Order crossover
5. Mutation
6. Elitism
7. Repeat until maximum generations

---

# Fitness Function

The fitness function minimizes the following objectives simultaneously:

- Total travel distance
- Priority delivery penalties
- Vehicle capacity penalties
- Maximum route distance penalties

Lower fitness values indicate better delivery routes.

---

# Healthcare Constraints

The original TSP implementation was extended with realistic logistics constraints:

### Priority Deliveries

Critical medications should be delivered earlier than regular supplies.

Priority levels:

- Priority 3 – Critical
- Priority 2 – Important
- Priority 1 – Regular

Late visits receive increasing penalties.

---

### Vehicle Capacity

Each vehicle has a maximum carrying capacity.

Routes exceeding the capacity receive a fitness penalty.

---

### Vehicle Autonomy

Vehicles have a maximum travel distance.

Long routes receive additional penalties to simulate fuel or battery limitations.

---

### Multiple Vehicles

Instead of implementing a complete Vehicle Routing Problem (VRP), the optimized route is divided among multiple vehicles.

This approach satisfies the project requirements while preserving the original Genetic Algorithm structure.

---

# Artificial Intelligence Integration

Google Gemini was integrated as a logistics assistant.

The LLM generates:

- Driver Instructions
- Daily Logistics Reports
- Vehicle Route Summaries
- Natural Language Question Answering

Example:

```
Question:

Which vehicle has the largest number of high-priority deliveries?

Answer:

Vehicle 2 has the highest number of high-priority deliveries.
```

---

# Route Visualization

The application displays:

- Healthcare locations
- Current best route
- Second-best route
- Fitness evolution graph

This allows visual monitoring of the optimization process.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Hasanessaad/medical-route-optimizer.git
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

Do **not** commit this file to Git.

---

# Running the Project

```bash
python src/tsp.py
```

The application will:

- Load the healthcare dataset
- Optimize delivery routes
- Display the visualization
- Generate vehicle summaries
- Generate AI driver instructions
- Generate the daily logistics report
- Answer logistics questions

---

# Results

Example configuration:

| Parameter | Value |
|-----------|------:|
| Locations | 90 |
| Vehicles | 3 |
| Population Size | 100 |
| Generations | 500 |
| Mutation Probability | 0.5 |

---

# Future Improvements

- Google Maps integration
- OpenStreetMap routing
- Real road distances
- Traffic-aware optimization
- Time-window constraints
- Dynamic routing
- Full Vehicle Routing Problem (VRP)
- Multiple depots

---

# Authors

**Hasan Essaad**

FIAP – Tech Challenge

Medical Route Optimization using Genetic Algorithms and Large Language Models

---

# License

This project was developed for educational purposes as part of the FIAP Tech Challenge.