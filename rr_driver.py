from rr_classes import User

# Create a new user and add some tasks
user = User('John', 'Doe')
user.add_task('task 1', 3)
user.add_task('task 2', 1)
user.add_task('task 3', 2)

user.complete_task()

# DRIVER

# Print User To Do Tasks (PQ)
user.to_do_tasks.print_queue()

print("")

# Print User Completed Tasks (Stack)
user.completed_tasks.print_stack()




