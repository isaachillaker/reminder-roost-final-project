from rr_classes import User

# Create a user
user = User("Bob", "Smith")

# Add three '3' tasks for the user to complete
user.add_task("Do homework", 2)
user.add_task("Go grocery shopping", 3)
user.add_task("Take kids to school", 1)

# to_do_tasks (PQ)
print("YOUR TASKS - (Queue)")
user.to_do_tasks.print_queue()

print("")

# Complete highest priority task
user.complete_task()

# completed_tasks (Stack)
print("COMPLETED TASKS - (Stack)")
user.completed_tasks.print_stack()

print("")

# to_do_tasks (PQ)
print("YOUR TASKS - (Queue)")
user.to_do_tasks.print_queue()



