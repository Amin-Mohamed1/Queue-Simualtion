import numpy as np
import matplotlib.pyplot as plt


# Function to generate arrival times
def generate_arrival_times(lambda_val, time_limit):
    BUFFER = 5
    arrival_times = np.cumsum(generate_exponential_times(lambda_val, int(time_limit * lambda_val * BUFFER)))
    return arrival_times[arrival_times <= time_limit]


# Function to generate exponential and service times
def generate_exponential_times(rate, size):
    return np.random.exponential(1 / rate, size)


def plot(Lambda, Meu1, Meu2, running_time, q1_initial):
    simulation_tuple = run_tandem(Lambda, Meu1, Meu2, running_time, q1_initial)
    l1 = []
    l2 = []
    time = []
    for i in range(len(simulation_tuple)):
        l1.append(simulation_tuple[i][0])
        l2.append(simulation_tuple[i][1])
        time.append(i)
    plt.figure()
    plt.plot(time, l1, label='Queue 1')
    plt.plot(time, l2, label='Queue 2')
    plt.xlabel('Time')
    plt.ylabel('Number of Customers')
    plt.legend()
    plt.title(
        f'Queue Length vs Time for Lambda={Lambda}, Meu1={Meu1}, Meu2={Meu2}, T={running_time}, q1_initial={q1_initial}'
    )
    plt.show()


def integrate(simulation_tuple, running_time):
    integration_value = 0
    for i in range(len(simulation_tuple) - 1):
        delta_t = simulation_tuple[i + 1][0] - simulation_tuple[i][0]
        integration_value += (simulation_tuple[i][1] + simulation_tuple[i][2]) * delta_t
    return integration_value / running_time


def run_tandem(lambda_rate, mu1_rate, mu2_rate, running_time, initial_number_of_customers):
    return []


def simulate_runs(lambda_rate, mu1_rate, mu2_rate, running_time, N):
    results = []
    q1_initial = 0
    for i in range(N):
        simulation_tuple = run_tandem(lambda_rate, mu1_rate, mu2_rate, running_time, q1_initial)
        plot(lambda_rate, mu1_rate, mu2_rate, running_time, q1_initial)
        results.append(integrate(simulation_tuple, running_time))
    return np.mean(results)


def main():
    # Define the parameters for the simulation
    lambda_values = [1, 5]
    mu1_values = [2, 4]
    mu2_values = [3, 4]
    T_values = [10, 50, 100, 1000]

    # Run the simulations for each combination of parameters
    for lambda_val in lambda_values:
        for mu1_val in mu1_values:
            for mu2_val in mu2_values:
                for T in T_values:
                    # Perform the simulation
                    expected_customers = simulate_runs(lambda_val, mu1_val, mu2_val, T, 100)

                    # Log the results
                    print(f'T={T}, lambda={lambda_val}, mu1={mu1_val}, mu2={mu2_val}, expected number of customers={expected_customers}')


# Entry point of the script
if __name__ == "__main__":
    main()
