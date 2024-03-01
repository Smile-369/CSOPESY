class Process:
    def __init__(self, pid, arrivalTime, burstTime):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.burstTimeRemaining = burstTime
        self.completionTime = 0
        self.turnaroundTime = 0
        self.waitingTime = 0
        self.isComplete = False
        self.inQueue = False

def queueUpdation(queue, timer, arrival, n, maxProcessIndex):
    zeroIndex = -1
    for i in range(n):
        if queue[i] == 0:
            zeroIndex = i
            break
    if zeroIndex == -1:
        return
    if maxProcessIndex < n:
        queue[zeroIndex] = maxProcessIndex + 1

def checkNewArrival(timer, arrival, n, maxProcessIndex, queue):
    if timer <= arrival[n - 1]:
        newArrival = False
        for j in range(maxProcessIndex + 1, n):
            if arrival[j] <= timer:
                if maxProcessIndex < j:
                    maxProcessIndex = j
                    newArrival = True
        if newArrival:
            queueUpdation(queue, timer, arrival, n, maxProcessIndex)

def queueMaintenance(queue, n):
    for i in range(n - 1):
        if queue[i + 1] != 0:
            queue[i], queue[i + 1] = queue[i + 1], queue[i]

def roundRobin(n, tq, arrival, burst):
    timer = 0
    maxProcessIndex = 0
    avgWait = 0
    avgTT = 0

    wait = [0] * n
    turn = [0] * n
    queue = [0] * n
    tempBurst = burst[:]

    complete = [False] * n
    for i in range(n):
        while timer < arrival[0]:
            timer += 1
        queue[0] = 1
        while True:
            flag = True
            for i in range(n):
                if tempBurst[i] != 0:
                    flag = False
                    break
            if flag:
                break
            for i in range(n):
                if queue[i] != 0:
                    ctr = 0
                    while ctr < tq and tempBurst[queue[0] - 1] > 0:
                        tempBurst[queue[0] - 1] -= 1
                        timer += 1
                        ctr += 1
                        checkNewArrival(timer, arrival, n, maxProcessIndex, queue)
                    if tempBurst[queue[0] - 1] == 0 and not complete[queue[0] - 1]:
                        turn[queue[0] - 1] = timer
                        complete[queue[0] - 1] = True
                    idle = True
                    if queue[n - 1] == 0:
                        for k in range(n):
                            if queue[k] != 0:
                                if not complete[queue[k] - 1]:
                                    idle = False
                    else:
                        idle = False
                    if idle:
                        timer += 1
                        checkNewArrival(timer, arrival, n, maxProcessIndex, queue)
                    queueMaintenance(queue, n)

    for i in range(n):
        turn[i] = turn[i] - arrival[i]
        wait[i] = turn[i] - burst[i]

    print("\nProgram No.\tArrival Time\tBurst Time\tWait Time\tTurnAround Time")
    for i in range(n):
        print(f"{i + 1}\t\t{arrival[i]}\t\t{burst[i]}\t\t{wait[i]}\t\t{turn[i]}")

    for i in range(n):
        avgWait += wait[i]
        avgTT += turn[i]

    print(f"\nAverage wait time : {avgWait / n}")
    print(f"Average Turn Around Time : {avgTT / n}")

if __name__ == "__main__":
    print("Enter the time quanta :", end=" ")
    tq = int(input())
    print("Enter the number of processes :", end=" ")
    n = int(input())

    arrival = []
    burst = []

    print("Enter the arrival time of the processes :", end=" ")
    arrival = list(map(int, input().split()))

    print("Enter the burst time of the processes :", end=" ")
    burst = list(map(int, input().split()))

    roundRobin(n, tq, arrival, burst)
