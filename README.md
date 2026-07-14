# Medical Route Optimization using Genetic Algorithms and Large Language Models

## Overview

This project was developed as part of the **FIAP Tech Challenge** for the Medical AI module.

The objective is to optimize the distribution of medications and medical supplies between healthcare facilities using a **Genetic Algorithm (GA)** while integrating a **Large Language Model (LLM)** to automatically generate driver instructions, operational reports, and answer logistics-related questions.

The project extends a basic Travelling Salesman Problem (TSP) implementation by incorporating realistic healthcare logistics constraints, making the optimization process closer to real-world medical distribution scenarios.

---

# Features

- Genetic Algorithm for route optimization
- Real healthcare dataset (90 healthcare locations)
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
- Vehicle route summaries
- Natural language route analysis using Google Gemini

---

# Technologies

- Python 3.12
- Pygame
- NumPy
- Pandas
- Google Gemini API
- Python Dotenv
- Git
- GitHub

---

# Project Structure

```text
medical-route-optimizer/

│
├── data/
│   └── foz_healthcare_locations.csv
│
├── outputs/
│   ├── driver_instructions/
│   └── reports/
│
├── src/
│   ├── tsp.py
│   ├── genetic_algorithm.py
│   ├── simulation.py
│   ├── llm.py
│   ├── data_loader.py
│   ├── draw_functions.py
│   ├── benchmark_att48.py
│   └── test_llm.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── .env (not included in Git)
```

---

# Project Architecture

```text
                 Healthcare Dataset
                        │
                        ▼
              Data Loading Module
                        │
                        ▼
           Genetic Algorithm Optimizer
     ┌──────────────┬──────────────┬──────────────┐
     │              │              │
     ▼              ▼              ▼
Tournament     Order Crossover   Mutation
 Selection
     │
     ▼
 Best Optimized Route
     │
     ▼
Vehicle Route Splitter (VRP)
     │
     ▼
 Vehicle Statistics
     │
     ▼
 Google Gemini API
 ├── Driver Instructions
 ├── Daily Reports
 ├── Route Summaries
 └── Question Answering
```

---

# How the System Works

```text
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
        ├── Tournament Selection
        ├── Order Crossover
        ├── Swap Mutation
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
Google Gemini
        ├── Driver Instructions
        ├── Daily Logistics Report
        ├── Route Summaries
        └── Natural Language Question Answering
```

---

# Genetic Algorithm

Each chromosome represents an ordered sequence of healthcare locations.

The optimization process follows the classical Genetic Algorithm cycle:

1. Generate an initial random population
2. Evaluate the fitness of every route
3. Select parents using Tournament Selection
4. Generate offspring using Order Crossover
5. Apply Swap Mutation
6. Preserve the best solution using Elitism
7. Repeat for the specified number of generations

---

# Fitness Function

The objective is to minimize the following fitness function:

**Fitness = Distance + Priority Penalty + Capacity Penalty + Distance Penalty**

The algorithm simultaneously minimizes:

- Total travel distance
- Delivery priority penalties
- Vehicle capacity violations
- Maximum route distance violations

Lower fitness values indicate better delivery routes.

---

# Healthcare Constraints

The original TSP implementation was extended with realistic healthcare logistics constraints.

## Priority Deliveries

Critical deliveries should be completed before regular deliveries.

Priority levels:

- **Priority 3** – Critical
- **Priority 2** – Important
- **Priority 1** – Regular

Late visits receive increasing penalties.

---

## Vehicle Capacity

Each vehicle has a maximum carrying capacity.

Routes exceeding the allowed weight receive an additional fitness penalty.

---

## Vehicle Autonomy

Vehicles have a maximum travel distance.

Routes exceeding this distance receive an additional penalty, simulating fuel or battery limitations.

---

## Multiple Vehicles

Instead of implementing a complete Vehicle Routing Problem (VRP), the optimized route is divided among multiple delivery vehicles.

This extension satisfies the project requirements while preserving the original Genetic Algorithm structure.

---

# Artificial Intelligence Integration

Google Gemini was integrated as a logistics assistant.

The Large Language Model automatically generates:

- Driver Instructions
- Daily Logistics Reports
- Vehicle Route Summaries
- Natural Language Question Answering

Example:

```text
Question:

Which vehicle has the highest number of high-priority deliveries?

Answer:

Vehicle 2 has the highest number of high-priority deliveries.
```

---

# API Documentation

The project integrates the **Google Gemini API** to provide intelligent logistics assistance.

## Implemented Functions

| Function | Description |
|----------|-------------|
| `generate_driver_instructions()` | Generates detailed delivery instructions for each vehicle. |
| `explain_vehicle_route()` | Summarizes the optimized route of each vehicle. |
| `generate_daily_report()` | Generates a professional logistics report from the optimization results. |
| `ask_question()` | Answers logistics-related questions using the optimized routes. |

## Authentication

The API key is stored securely using environment variables.

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

The `.env` file should never be committed to Git.

---

# Demonstration Scripts

The repository includes demonstration scripts for testing the project.

## tsp.py

Main application.

It performs:

- Healthcare dataset loading
- Genetic Algorithm optimization
- Route visualization
- Vehicle route splitting
- Driver instruction generation
- Daily report generation
- Natural language question answering

Run:

```bash
python src/tsp.py
```

---

## test_llm.py

Demonstrates the Google Gemini integration independently of the optimization algorithm.

Functions demonstrated:

- Driver instruction generation
- Logistics report generation
- Natural language interaction

Run:

```bash
python src/test_llm.py
```

---

# Route Visualization

The application provides a real-time visualization of the optimization process.

The interface displays:

- Healthcare locations
- Current best route
- Secondary candidate route
- Fitness evolution graph

This visualization allows users to observe how the Genetic Algorithm improves delivery routes over successive generations.

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

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

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

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Do **not** commit this file to Git.

---

# Running the Project

Execute:

```bash
python src/tsp.py
```

The application will:

- Load the healthcare dataset
- Execute the Genetic Algorithm
- Visualize the optimization process
- Split routes among vehicles
- Generate vehicle summaries
- Generate AI driver instructions
- Generate the daily logistics report
- Answer logistics questions

---

# Example Results

| Parameter | Value |
|-----------|------:|
| Healthcare Locations | 90 |
| Vehicles | 3 |
| Population Size | 100 |
| Generations | 500 |
| Mutation Probability | 0.5 |

---

# Future Improvements

- Google Maps integration
- OpenStreetMap road routing
- Real road-distance calculations
- Traffic-aware route optimization
- Delivery time windows
- Dynamic routing
- Complete Vehicle Routing Problem (VRP)
- Multiple depots
- Cloud deployment

---

# Authors

**Hasan Essaad**

FIAP – Tech Challenge

Medical Route Optimization using Genetic Algorithms and Large Language Models

---

# License

This project was developed exclusively for educational purposes as part of the FIAP Tech Challenge.
