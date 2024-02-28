def round_robin_scheduling(processes, time_quantum):
    n = len(processes)
    total_time = sum(process[2] for process in processes)
    total_time_counted = 0
    wait_time = 0
    # Initialize remaining times
    remaining_times = [process[2] for process in processes]

    while total_time > 0:
        for i in range(n):
            if remaining_times[i] <= 0:
                continue

            if remaining_times[i] <= time_quantum:
                total_time_counted += remaining_times[i]
                total_time -= remaining_times[i]
                remaining_times[i] = 0
            else:
                total_time_counted += time_quantum
                total_time -= time_quantum
                remaining_times[i] -= time_quantum

            if remaining_times[i] == 0:
                wait_time += total_time_counted - processes[i][1] - processes[i][2]

    avg_wait_time = wait_time / n

    print("\nRound Robin Scheduling Results:")
    for i in range(n):
        start_time = total_time_counted - processes[i][2] - (n - i) * time_quantum
        end_time = total_time_counted - (n - i - 1) * time_quantum
        print(f"P[{processes[i][0]}] start time: {start_time} end time: {end_time} | Waiting time: {wait_time / n}")
    print("Average waiting time:", round(avg_wait_time, 2))
