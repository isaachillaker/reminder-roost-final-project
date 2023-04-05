from rr_classes import User, PriorityQueue

# Create a new user and add some tasks
user = User('John', 'Doe')
user.add_task('task 1', 3)
user.add_task('task 2', 1)
user.add_task('task 3', 2)

# Complete tasks in order of priority
while True:
    task = user.complete_task()
    if task is None:
        break
    print(task)





