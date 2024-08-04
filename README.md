# Queue Simulation Project

This project simulates a tandem queueing system with two queues and a single server in each queue. The simulation models the arrival and service processes using exponential distributions, allowing the evaluation of system performance under various parameter configurations.

## Introduction

The tandem queueing system is a fundamental model in operations research and computer science, representing processes where tasks or customers move through a series of stages (queues) serviced by different servers. This project implements a simulation of such a system to study the behavior of queue lengths over time and understand the impact of different arrival and service rates.

The system consists of:
- **Arrival Process**: Customers arrive according to a Poisson process with a given rate `λ`.
- **Service Process**: Each server processes customers with exponentially distributed service times characterized by rates `μ1` and `μ2`.

## Project Structure

- **`main.py`**: Contains the main simulation logic, including the functions for generating interarrival and service times, running the simulation, and plotting the results.
- **`README.md`**: This file, describing the project, usage, and structure.

## Main Logic

The core logic of the simulation involves the following steps:

1. **Generate Interarrival and Service Times**:
    - Interarrival times are generated using an exponential distribution with the rate parameter `λ`.
    - Service times for both queues are generated using exponential distributions with rates `μ1` and `μ2`.

2. **Simulation Execution**:
    - The simulation runs for a specified duration (`T`), tracking the number of customers in each queue over time.
    - Events include arrivals, service completions at the first server, and service completions at the second server.
    - The state of the system (number of customers in each queue) is recorded at each event.

3. **Plotting and Analysis**:
    - The number of customers in each queue is plotted over time to visualize the queue dynamics.
    - The average number of customers in the system is calculated by integrating the area under the curve of the queue length over time.


## Simulation Parameters

- `λ (lambda_values)`: Arrival rates to the system.
- `μ1 (mu1_values)`: Service rates for the first queue.
- `μ2 (mu2_values)`: Service rates for the second queue.
- `T_values`: Simulation time for each run.
- `N`: Number of simulation runs.
