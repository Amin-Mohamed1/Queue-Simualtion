import numpy as np
import matplotlib.pyplot as plt


# Function to generate arrival times
def generate_interarrival_times(arrival_rate, max_time):
    times = []
    current_time = 0
    while current_time < max_time:
        interarrival = np.random.exponential(1 / arrival_rate)
        current_time += interarrival
        times.append(current_time)
    return np.array(times)


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


def run_tandem(arrival_rate, dep_rate1, dep_rate2, trial, initial_capacity):
    # Generate interarrival times based on the arrival rate and trial duration
    interarrival_times = generate_interarrival_times(arrival_rate, trial)
    service_duration1 = generate_exponential_times(dep_rate1, len(interarrival_times) + initial_capacity) # get service time of first queue
    service_duration2 = generate_exponential_times(dep_rate2, len(interarrival_times) + initial_capacity) # get service time of second queue

    current_time = 0
    # if the first queue is initially not empty
    queue_first = initial_capacity
    queue_second = 0

    # Initialize system state to store tuples of (time, queue1 length, queue2 length)
    system_state = []
    arrival_index = 0

    # Initialize next arrival and service end times
    next_arrival = interarrival_times[0] if len(interarrival_times) > 0 else float('inf')
    next_service1_end = current_time + service_duration1[0] if queue_first > 0 else float('inf')
    next_service2_end = float('inf')
    service_index1 = 0
    service_index2 = 0

    while current_time < trial :
        # Determine the time of the next event (arrival or service completion)
        next_event_time = min(next_arrival, next_service1_end, next_service2_end)

        # If the next event is in the future, record the current system state
        if next_event_time > current_time:
            system_state.append((current_time, queue_first, queue_second))
        # Advance the current time to the next event
        current_time = next_event_time
        # Handle arrival event
        if next_event_time == next_arrival:
            queue_first += 1
            arrival_index += 1
            next_arrival = interarrival_times[arrival_index] if arrival_index < len(interarrival_times) else float('inf')
            if queue_first == 1 and next_service1_end == float('inf'):
                next_service1_end = current_time + service_duration1[service_index1]

        # Handle service completion at server 1
        if next_event_time == next_service1_end:
            queue_first -= 1
            queue_second += 1
            service_index1 += 1
            next_service1_end = current_time + service_duration1[service_index1] if queue_first > 0 else float('inf')
            if queue_second == 1 and next_service2_end == float('inf'):
                next_service2_end = current_time + service_duration2[service_index2]

        # Handle service completion at server 2
        if next_event_time == next_service2_end:
            queue_second -= 1
            service_index2 += 1
            next_service2_end = current_time + service_duration2[service_index2] if queue_second > 0 else float('inf')
    return system_state


def simulate_runs(lambda_rate, mu1_rate, mu2_rate, running_time, N ,q1_initial):
    results = []
    for i in range(N):
        simulation_tuple = run_tandem(lambda_rate, mu1_rate, mu2_rate, running_time, q1_initial)
        results.append(integrate(simulation_tuple, running_time))
        plot(lambda_rate, mu1_rate, mu2_rate, running_time, q1_initial)
    return np.mean(results)

def main(q1_initial):
    # Define the parameters for the simulation
    lambda_values = [1, 5]
    mu1_values = [2, 4]
    mu2_values = [3, 4]
    T_values = [10 ,50 , 100 , 1000]

    # Run the simulations for each combination of parameters
    for lambda_val in lambda_values:
        for mu1_val in mu1_values:
            for mu2_val in mu2_values:
                average = 0
                for T in T_values:
                    # Perform the simulation
                    expected_customers = simulate_runs(lambda_val, mu1_val, mu2_val, T,1000 ,q1_initial)
                    average += expected_customers
                    # Log the results
                    print(f'simulation time={T}, λ={lambda_val}, μ1={mu1_val}, μ2={mu2_val}, number of customer in total system={expected_customers}')
                print(
                    f'Average -> λ={lambda_val}, μ1={mu1_val}, μ2={mu2_val}, number of customer in total system={average/4}')
                print("\n")


# Entry point of the script
if __name__ == "__main__":
    main(0) # q1_initial = 0 -> part a
    print("\n")
    print("\n")
    main(2000) # q1_initial = 2000 -> part b
