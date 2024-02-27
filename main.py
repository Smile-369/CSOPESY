import numpy as np
def process_input_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            #first line
            x, y, z = map(int, file.readline().split())

            if x != 3:
                z = 1

            #specs constraints
            if not (0 <= x <= 3 and 3 <= y <= 100 and (1 <= z <= 100 or x != 3)):
                print("Invalid input.")
                return None

            processes = []
            for _ in range(y):
                a, b, c = map(int, file.readline().split())
                processes.append((a, b, c))

            return x, y, z, processes

    except FileNotFoundError:
        print(f"{file_name} not found.")
        return None

def getWaitingTime(processes,waitingTime,n):
    rt = [0] * n
    for i in range(n):
        rt[i] = processes[i][2]
    complete = 0
    t = 0
    minm = 10000
    short = 0
    check = False
    while (complete != n):
        for j in range(n):
            if ((processes[j][1] <= t) and (rt[j] < minm) and rt[j] > 0):
                minm = rt[j]
                short = j
                check = True
        if (check == False):
            t += 1
            continue
        rt[short] -= 1
        minm = rt[short]
        if (minm == 0):
            minm = 10000
        if (rt[short] == 0):
            complete += 1
            check = False
            fint = t + 1
            waitingTime[short] = (fint - processes[short][1] - processes[short][2])
            if (waitingTime[short] < 0):
                waitingTime[short] = 0
        t += 1

def getTurnAroundTime(processes,waitingTime,turnAroundTime,n):
    for i in range(n):
        turnAroundTime[i] = processes[i][2] + waitingTime[i]

def getStartTime(processes,waitingTime,startTime,n):
    for i in range(n):
        startTime[i] = (processes[i][1] + waitingTime[i])-1

#First Come, First Served 
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x[1])  # Sort processes by arrival time
    completion_time = [0] * len(processes)
    waiting_time = [0] * len(processes)

    gantt_chart = []  # Array to store the Gantt chart

    completion_time[0] = processes[0][1] + processes[0][2]
    waiting_time[0] = 0

    gantt_chart.extend([processes[0][0]] * processes[0][2])

    for i in range(1, len(processes)):
        completion_time[i] = max(completion_time[i - 1], processes[i][1]) + processes[i][2]
        waiting_time[i] = completion_time[i - 1] - processes[i][1]

        gantt_chart.extend([processes[i][0]] * (processes[i][1] - completion_time[i - 1]))
        gantt_chart.extend([processes[i][0]] * processes[i][2])

    average_waiting_time = sum(waiting_time) / len(waiting_time)

    print("\nFCFS Scheduling Results:")
    for i in range(len(processes)):
        print(f"P[{processes[i][0]}] start time: {completion_time[i] - processes[i][2]} end time: {completion_time[i]} | Waiting time: {waiting_time[i]}")

    print("Average waiting time:", average_waiting_time)

    print("\nGantt Chart:")
    print("|", end="")
    for item in gantt_chart:
        print(f" P{item} |", end="")
    print()

#Shortest Remaining Time First      
def srtf_scheduling(processes):
    # Sort processes by arrival time
    n=len(processes)
    waiting_time=[0]*n
    completion_time=[0]*n
    start_time=[0]*n

    getWaitingTime(processes,waiting_time,n)
    getTurnAroundTime(processes,waiting_time,completion_time,n)

    gantt_chart = []  # Array to store the Gantt chart
    getStartTime(processes,waiting_time,start_time,n)


   
    average_waiting_time = sum(waiting_time) / len(waiting_time)
    
    print("\nSRTF Scheduling Results:")
    for i in range(n):
        print(f"P[{processes[i][0]}] start time: {start_time[i]} end time: {completion_time[i]} | Waiting time: {waiting_time[i]}")

    zipped_processes= sorted(zip(start_time,processes))
    sorted_processes=[element for _, element in zipped_processes]

    for i in range(len(processes)):
        gantt_chart.extend([sorted_processes[i][0]] * (sorted_processes[i][1] - completion_time[i - 1]))
        gantt_chart.extend([sorted_processes[i][0]] * sorted_processes[i][2])

    print("Average waiting time:", average_waiting_time)
    
    print("\nGantt Chart:")
    print("|", end="")
    for item in gantt_chart:
        print(f" P{item} |", end="")
    print()

#Round Robin
def round_robin_scheduling(processes, quantum): 
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    time =   0
    processes_executed =   0

    # Sort processes by arrival time
    processes = sorted(processes, key=lambda x: x[1])

    # Initialize remaining burst times
    remaining_burst_times = [process[2] for process in processes]

    while processes_executed < n:
        for i in range(n):
            if processes[i][1] <= time:  # Check if process has arrived
                if remaining_burst_times[i] <= quantum:  # Check if process can be executed in the current quantum
                    time += remaining_burst_times[i]
                    waiting_time[i] = time - processes[i][1] - processes[i][2]
                    remaining_burst_times[i] =  0
                    processes_executed +=   1
                else:
                    # Process needs more time than quantum
                    time += quantum
                    waiting_time[i] = time - processes[i][1] - quantum
                    remaining_burst_times[i] -= quantum
            else:
                # Process has not arrived yet
                break

        # Check if any process has not been executed yet
        if processes_executed < n:
            time +=   1  # Increment time to allow other processes to execute

    # Calculate turnaround time
    for i in range(n):
        turnaround_time[i] = waiting_time[i] + processes[i][2]

    # Print scheduling results
    print("\nRound Robin Scheduling Results:")
    for i in range(n):
        print(f"P[{processes[i][0]}] start time: {time - processes[i][2]} end time: {time} | Waiting time: {waiting_time[i]} Turnaround time: {turnaround_time[i]}")

    # Calculate average waiting time and turnaround time
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    print(f"Average waiting time: {avg_waiting_time}")
    print(f"Average turnaround time: {avg_turnaround_time}")

    gantt_chart = []
    for i in range(n):
        gantt_chart.extend([processes[i][0]] * (time - processes[i][2] - completion_time[i]))
        gantt_chart.extend([processes[i][0]] * (processes[i][2] - remaining_burst_times[i]))

    print("\nGantt Chart:")
    print("|", end="")
    for item in gantt_chart:
        print(f" P{item} |", end="")
    print()


file_name = input("Enter the name of the input text file: ")
input_data = process_input_from_file(file_name)

if input_data:
    x, y, z, processes = input_data
    fcfs_scheduling(processes)
    srtf_scheduling(processes)
    round_robin_scheduling(processes, 2)

