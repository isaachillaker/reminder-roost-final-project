from rr_classes import PriorityQueue

# Create a priority queue and add some tasks
q = PriorityQueue()
q.push('task 1', 3)
q.push('task 2', 1)
q.push('task 3', 2)

# Process the tasks in order of priority
while len(q) > 0:
    task = q.pop()
    print(task)
