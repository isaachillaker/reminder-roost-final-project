import heapq
import re
from tkinter import *


class User:
    def __init__(self, first_name=None, last_name=None):
        if first_name is None:
            first_name = self.get_valid_name("Enter your first name:")
        if last_name is None:
            last_name = self.get_valid_name("Enter your last name: ")
        self.first_name = first_name
        self.last_name = last_name
        self.to_do_tasks = PriorityQueue()
        self.completed_tasks = Stack()
        self.deleted_tasks = Stack()

    # MISSING UNIT TEST!
    def get_valid_name(self, name):
        """
        This method is called when a new User object is created and no values are assigned to
        its 'first_name' or 'last_name' variables. It calls the validate_name() method to
        validate that the names being passed are strings that contain only letters or the special
        characters " - " or " ' "
        """
        while True:
            name = input(f"{name}")
            try:
                validated_name = self.validate_name(name)
                return validated_name
            except ValueError as e:
                print(e)

    # MISSING UNIT TEST!
    def validate_name(self, name):
        """
        This method is used to validate the 'first_name' and 'last_name' attributes
        of the User class. It ensures that the value being passed is a String containing
        only letters and/or special the special characters " - " or " ' ".
        """
        # Check that the name contains only letters and allowed symbols
        if not re.match(r'^[A-Za-z\'\- ]+$', name):
            raise ValueError('Invalid name: only letters, "-" and "\'" allowed')
        return name.strip()

    def add_task(self, task=None, priority=None):
        """
        THis method adds a task to the 'to_do_tasks' PQ object.

        1) An error msg is returned if one of the arguments is left blank.

        2) If arguments are satisfied, push the new task into the 'to_do_tasks' PQ object.

        :param task: The name of the task (string)
        :param priority: The priority level of the task (integer)
        """
        # 1
        error_msg = "Both task and priority must be specified!"
        if task is None or priority is None:
            return error_msg
        # 2
        self.to_do_tasks.push(task, priority)

    def complete_task(self, task=None):
        """
        This method is used to 'complete' a task. One argument 'task' set to None by default. The argument
        being passed is the task that the user wants to mark as complete.

        1) If the 'task' argument is 'None', meaning no argument has been passed, then
        the program utilizes 'to_do_tasks' pop() method, removing the task from the
        queue. The 'completed_tasks' push() method is then used to add this completed
        task to the completed Stack.

        2) If an argument IS passed to the method, then that specific item is removed from the queue,
        regardless of its priority level. It is then added to the 'completed_tasks' Stack object.
        """
        # 1
        if task is None:
            if len(self.to_do_tasks) == 0:
                return None
            completed_task = self.to_do_tasks.pop()
            self.completed_tasks.push(completed_task)
            return completed_task
        # 2
        else:
            for priority, index, item in self.to_do_tasks._queue:
                if item == task:
                    self.to_do_tasks._queue.remove((priority, index, item))
                    self.completed_tasks.push(item)
                    return item
            return None

    def delete_task(self, task):
        """
        This method removes a specified task from the 'to_do_tasks' PQ object. It is then moved into
        the 'deleted_tasks' Stack object.

        Use a for loop to traverse the PQ object, returning the 'item' attribute that matches the
        task argument given by the user. If there is a match, then that task is removed from the PQ
        object and pushed into the 'deleted_tasks' Stack object.

        :param task: Task to be deleted, its name
        """
        for priority, index, item in self.to_do_tasks._queue:
            if item == task:
                self.to_do_tasks._queue.remove((priority, index, item))
                self.deleted_tasks.push((-priority, index, item))
                return (priority, index, item)

    def undo(self):
        if len(self.deleted_tasks) > 0:
            priority, index, task = self.deleted_tasks.pop()
            self.to_do_tasks.push(task, priority)
            return task


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def print_queue(self):
        for _, _, item in sorted(self._queue):
            print(item)

    def queue(self):
        return [item for _, _, item in sorted(self._queue)]

    def __len__(self):
        return len(self._queue)


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if len(self._items) == 0:
            raise IndexError('pop from empty stack')
        return self._items.pop()

    def peek(self):
        if len(self._items) == 0:
            raise IndexError('peek from empty stack')
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def print_stack(self):
        for item in reversed(self._items):
            print(item)

    def __len__(self):
        return len(self._items)


class GUI:
    def __init__(self, root):
        self.root = root
        root.title("Task Manager")
        root.geometry('600x750')

        self.user = User("Isaac", "Hillaker")  # create a User object

        self.heading_label = Label(root, text=f"{self.user.first_name}'s tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.pack()

        self.instructions_label = Label(root,
                                        text="Type in a task then click the 'Add Task' button to add your new task.",
                                        font=("Helvetica", 12))
        self.instructions_label.pack()

        # create task entry box and add task button
        self.task_label_1 = Label(root,
                                  text="Task name:",
                                  font=("Helvetica", 12))
        self.task_label_1.pack()

        # TASK NAME ENTRY
        self.task_1_entry = Entry(root, width=25)
        self.task_1_entry.pack()
        self.task_label_2 = Label(root,
                                  text="Task priority level (1, 2, or 3):",
                                  font=("Helvetica", 12))
        self.task_label_2.pack()
        self.invalid_input_label = Label(root, fg="red")
        self.invalid_input_label.pack()

        # PRIORITY LEVEL ENTRY
        self.task_2_entry = Entry(root, width=25)
        self.task_2_entry.pack()

        # BUTTONS
        # ADD TASK button
        self.add_button = Button(root, width=10, height=2, bg="green", fg="white", text="Add Task",
                                 command=self.add_task)
        self.add_button.pack()
        # DELETE TASK button
        self.remove_button = Button(root, width=10, height=2, bg="red", fg="white", text="Delete Task",
                                    command=self.delete_task)
        self.remove_button.pack()

        # UNDO button
        self.undo_button = Button(root, width=10, height=2, bg="yellow", fg="black", text="Undo Deletion",
                                  command=self.undo_deletion)
        self.undo_button.pack()

        # create listbox for tasks
        self.heading_label = Label(root, text="To-Do Tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.pack()
        self.tasks_listbox = Listbox(root, width=50)
        self.tasks_listbox.pack()

        # create listbox for completed tasks
        # self.heading_label = Label(root, text="Completed Tasks", font=("Helvetica", 18, "bold"))
        # self.heading_label.pack()
        # self.completed_listbox = Listbox(root, width=50)
        # self.completed_listbox.pack()

        # create listbox for deleted tasks
        self.heading_label = Label(root, text="Deleted Tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.pack()
        self.deleted_tasks_listbox = Listbox(root, width=50)
        self.deleted_tasks_listbox.pack()

    def add_task(self):
        """
        This method adds a new task to the To Do List section of the GUI.

        1) Ensure that if an error label is present, that it is removed with this method is called
        2) Grab the contents of the two entry widgets and give them meaningful names
        3) Ensure that the 'priority' input is a digit (by default it is entered as a string, so first we check
        that the string contains only digits.
        3.5) If the 'priority' input does NOT contain digits, return an error label to the GUI and prompt
        user for new input.
        4) Ensure that the digits are converted to integers
        5) Ensure that the input entered is a 1, 2, or 3.
        6) We add the task to the User object's PriorityQueue object by calling the 'add_task' method of the User. We
        then delete the input from the entry widget boxes, so that the user can enter new data. We finally call the
        update_listbox() method of the GUI class and populate the listbox with the latest data from the User object's
        PriorityQueue.

        """
        # 1
        if self.invalid_input_label:
            self.invalid_input_label.config(text="")

        # 2
        task_name = self.task_1_entry.get()
        task_priority = self.task_2_entry.get()

        # 3
        # Ensure that 'priority' is an integer
        if task_priority.isdigit():
            # 4
            task_priority = int(task_priority)
            # 5
            if task_priority in range(1, 4):
                # 6
                # add task to the user's task list
                self.user.add_task(task_name, task_priority)
                # Remove input values from the entry boxes
                self.task_1_entry.delete(0, END)
                self.task_2_entry.delete(0, END)
                # Update the listbox to reflect newly added tasks and their priority levels
                self.update_listbox()
            else:
                self.invalid_input_label.config(text="Number out of range. Must be a 1, 2, or 3!")
        # 3.5
        else:
            self.invalid_input_label.config(text="Must be a number: 1, 2, or 3!")

    def update_listbox(self):
        """
        When a new task is successfully added to the to do list, this method will update
        the listbox to reflect those changes. Any new items added to the listbox will
        be sorted by their priority number (with 1's on the bottom, 2's in the middle, and
        3's on the top).

        1) Delete old listbox contents
        2) Access the User object's '_queue' attribute (a list)
        3) Loop through the current version of the Users' '_queue' list and
        add them to the new listbox
        """
        # 1
        self.tasks_listbox.delete(0, END)
        # 2
        pq = self.user.to_do_tasks
        task_list = pq._queue
        # 3
        for _, priority, name in task_list:
            self.tasks_listbox.insert(END, name)

    def delete_task(self):
        """
        This method deletes a task from the To-Do listbox and moves it
        to the Deleted Tasks listbox. It also deletes the task from the User object's
        'to_do_list' PQ object and moves it to the 'deleted_tasks' Stack object.
        """

        # Check if an item is selected in the tasks listbox
        if not self.tasks_listbox.curselection():
            return

        # Get the selected item from the tasks listbox
        selected_item = self.tasks_listbox.get(self.tasks_listbox.curselection())

        # Update User object to update 'to_do_tasks' task removal
        self.user.delete_task(selected_item)

        # Remove the selected item from the tasks listbox
        self.tasks_listbox.delete(self.tasks_listbox.curselection())

        # Add the selected item to the deleted task listbox
        self.deleted_tasks_listbox.insert(END, selected_item)

        # Update the To-Do listbox to make sure remaining items are ordered
        self.update_listbox()

    def undo_deletion(self):
        # Get last deleted item from User object's 'deleted_tasks' Stack
        self.user.undo()

        # Remove the last item from the deleted tasks listbox
        self.deleted_tasks_listbox.delete(self.deleted_tasks_listbox.index(END) - 1)

        # Update the To-Do listbox to make sure remaining items are ordered
        self.update_listbox()
