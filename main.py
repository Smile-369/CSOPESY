import numpy as np
def process_input_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            x, n, q = map(int, file.readline().split())

            if x != 3:
                q = 1  # Ignoring time quantum if not Round Robin

            if not (0 <= x <= 3 and 3 <= n <= 100 and (1 <= q <= 100 or x != 3)):
                print("Invalid input.")
                return None

            processes = []
            for _ in range(n):
                a, b, c = map(int, file.readline().split())
                processes.append((a, b, c))

            return x, n, q, processes

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

def getCompletionTime(processes,startTime,completionTime,n):
    for i in range(n):
        completionTime[i] = processes[i][2] + startTime[i]

def getStartTime(processes,waitingTime,startTime,n):
    for i in range(n):
        startTime[i] = (processes[i][1] + waitingTime[i])

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

#Shortest Job First
def sjf_scheduling(processes):
    sorted_processes = sorted(processes, key=lambda x: x[1])

    completion_time = [0] * len(sorted_processes)
    waiting_time = [0] * len(sorted_processes)
    gantt_chart = []  # Array to store the Gantt chart
    start_times = [0] * len(sorted_processes)
    turn_around = [0] * len(sorted_processes)
    burst_time = [0] * len(sorted_processes)

    current_time = sorted_processes[0][1]  # Initialize the current time with the start time of the first process

    if sorted_processes[0][0] == 0:

        while sorted_processes:
            start_time = current_time
            eligible_processes = [p for p in sorted_processes if p[1] <= current_time]
            print(eligible_processes)

            if not eligible_processes:
                current_time += 1
                continue

            shortest_job = min(eligible_processes, key=lambda x: x[2])
            index = sorted_processes.index(shortest_job)

            if current_time < sorted_processes[index][1]:
                gantt_chart.extend([0] * (sorted_processes[index][1] - current_time))
                current_time = sorted_processes[index][1]

            gantt_chart.extend([sorted_processes[index][0]] * sorted_processes[index][2])
            current_time += sorted_processes[index][2]

            pro_index = shortest_job[0]
            completion_time[pro_index] = current_time
            turn_around[pro_index] = current_time - sorted_processes[index][1]
            burst_time[pro_index] = sorted_processes[index][2]
            waiting_time[pro_index] = turn_around[pro_index] - burst_time[pro_index]
            start_times[pro_index] = start_time

            sorted_processes.pop(index)
    
    else:
        while sorted_processes:
            start_time = current_time
            eligible_processes = [p for p in sorted_processes if p[1] <= current_time]
            print(eligible_processes)

            if not eligible_processes:
                current_time += 1
                continue

            shortest_job = min(eligible_processes, key=lambda x: x[2])
            index = sorted_processes.index(shortest_job)

            if current_time < sorted_processes[index][1]:
                gantt_chart.extend([0] * (sorted_processes[index][1] - current_time))
                current_time = sorted_processes[index][1]

            gantt_chart.extend([sorted_processes[index][0]] * sorted_processes[index][2])
            current_time += sorted_processes[index][2]

            pro_index = shortest_job[0]-1
            completion_time[pro_index] = current_time
            turn_around[pro_index] = current_time - sorted_processes[index][1]
            burst_time[pro_index] = sorted_processes[index][2]
            waiting_time[pro_index] = turn_around[pro_index] - burst_time[pro_index]
            start_times[pro_index] = start_time

            sorted_processes.pop(index)

    average_waiting_time = sum(waiting_time) / len(waiting_time)

    print("\nShortest Job First (SJF) Scheduling (Non-preemptive) Results:")
    for i in range(len(completion_time)):
        print(f"P[{processes[i][0]}] start time: {start_times[i]} end time: {completion_time[i]} | Waiting time: {waiting_time[i]}")

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
   

    gantt_chart = []  # Array to store the Gantt chart
    getStartTime(processes,waiting_time,start_time,n)
    getCompletionTime(processes,start_time,completion_time,n)

   
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
def queueUpdation(queue, timer, arrival, n, maxProccessIndex):
    zeroIndex = -1
    for i in range(n):
        if queue[i] == 0:
            zeroIndex = i
            break

    if zeroIndex == -1:
        return
    if maxProccessIndex < n:
        queue[zeroIndex] = maxProccessIndex + 1


def checkNewArrival(timer, arrival, n, maxProccessIndex, queue):
    if timer < arrival[n-1]:
        newArrival = False
        for j in range(maxProccessIndex+1, n):
            if arrival[j] <= timer:
                if maxProccessIndex < j:
                    maxProccessIndex = j
                    newArrival = True

        # adds the index of the arriving process(if any)
        if newArrival:
            queueUpdation(queue, timer, arrival, n, maxProccessIndex)


def queueMaintainence(queue, n):
    for i in range(n-1):
        if queue[i+1] != 0:
            queue[i], queue[i+1] = queue[i+1], queue[i]


def round_robin_scheduling(processes, tq):
    n = len(processes)
    avgWait, avgTT = 0, 0

    arrival = [p[1] for p in processes]
    burst = [p[2] for p in processes]
    temp_burst = burst.copy()
    wait = [0] * n
    turn = [0] * n
    complete = [False] * n
    queue = [0] * n
    maxProccessIndex = 0
    timer = 0

    while True:
        flag = True
        for i in range(n):
            if temp_burst[i] != 0:
                flag = False
                break

        if flag:
            break

        for i in range(n):
            if queue[i] != 0:
                ctr = 0
                while ctr < tq and temp_burst[queue[0]-1] > 0:
                    temp_burst[queue[0]-1] -= 1
                    timer += 1
                    ctr += 1

                    # Updating the ready queue until all the processes arrive
                    checkNewArrival(timer, arrival, n, maxProccessIndex, queue)

                if temp_burst[queue[0]-1] == 0 and not complete[queue[0]-1]:
                    # turn currently stores exit times
                    turn[queue[0]-1] = timer
                    complete[queue[0]-1] = True

                # checks whether or not CPU is idle
                idle = True
                for k in range(n):
                    if queue[k] != 0 and not complete[queue[k]-1]:
                        idle = False
                        break

                if idle:
                    timer += 1
                    checkNewArrival(timer, arrival, n, maxProccessIndex, queue)

                # Maintaining the entries of processes after each preemption in the ready Queue
                queueMaintainence(queue, n)

    for i in range(n):
        turn[i] = turn[i] - arrival[i]
        wait[i] = turn[i] - burst[i]

    print("\nRound Robin Scheduling Results:")
    for i in range(n):
        print(f"P[{processes[i][0]}] start time: {arrival[i]} end time: {turn[i] + arrival[i]} | Waiting time: {wait[i]}")

    for i in range(n):
        avgWait += wait[i]
        avgTT += turn[i]

    print("\nAverage wait time : ", (avgWait//n))
    print("\nAverage Turn Around Time : ", (avgTT//n))


if __name__ == '__main__':
    file_name = input("Enter the name of the input text file: ")
    input_data = process_input_from_file(file_name)

    if input_data:
        x, n, q, processes = input_data
        
        if x == 0:
            fcfs_scheduling(processes)
        elif x == 1:
            sjf_scheduling(processes)
        elif x == 2:
            srtf_scheduling(processes)
        elif x == 3:
            round_robin_scheduling(processes, q)
        else:
            print("Unsupported scheduling algorithm.")

