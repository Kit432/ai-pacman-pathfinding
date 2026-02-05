# AI Pathfinding Comparison (Pacman)

A comparative study of search algorithms implemented in **Python** to solve a 1D Pacman constraint satisfaction problem.

## Overview
This project implements and analyzes three fundamental pathfinding algorithms to navigate an autonomous agent (Pacman) through a grid environment containing targets (fruits) and hazards (poison).

The core goal is to demonstrate the trade-offs between **completeness**, **optimality**, and **resource usage** (Time vs. Space complexity).

## Algorithms Implemented
1.  **DFS (Depth-First Search):** Low memory footprint, fast for deep solutions, but non-optimal.
2.  **BFS (Breadth-First Search):** Guarantees optimal solution (shortest path), but high memory consumption.
3.  **Best-First Search (Heuristic):** Uses a custom heuristic function (Distance to Target + Hazard Avoidance) to guide the agent efficiently.

## Performance Benchmark
The project includes a benchmarking module using `tracemalloc` to measure real-time performance.

| Algorithm | Avg Steps | Time Efficiency | Memory Usage | Optimality |
|-----------|-----------|-----------------|--------------|------------|
| **DFS** | Low       | Fast            | Low (~0.2MB) | No         |
| **BFS** | High      | Slower          | High (~2.4MB)| **Yes** |
| **BestFS**| Low       | Fast            | Low (~0.2MB) | No         |
