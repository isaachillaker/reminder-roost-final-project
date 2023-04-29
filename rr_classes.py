"""
AUTHOR: Isaac Hillaker
ASSIGNMENT: Final Project: Task Manager
DATE: 04/28/2023
INFO:

    This program implements a Task Manager program by using four separate class: Stack, PriorityQueue, User, and GUI.
    A more detailed explanation of each can be found in the classes and their respective methods.

    There is driver code in rr_driver.py and unit tests in rr_unittests.py, both of which are located in
    this same directory.

I completed this assignment without any unauthorized assistance.
"""

import heapq
import re
from tkinter import *


class PriorityQueue:
    """
    This class implements a priority queue data structure using the heapq module, which relies on Python lists.

    The queue is initialized as an empty list and an index is set to 0. The index is used to ensure that items
    with the same priority are inserted in the order they were added
    """

    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        """
        Adding a task in this program requires a task name (item) and a priority level (priority) which must be 1, 2,
        or 3.

        This method takes an item and priority as arguments. The heappush method (built-in to heapq) inserts the item
        into the queue as a tuple, where a String (item) an Integer (priority), and an index are stored.
        """
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        """
        Returns the top item from the queue
        """
        return heapq.heappop(self._queue)[-1]

    def print_queue(self):
        """
        Iterates through the queue, returning all its items.
        """
        for _, _, item in sorted(self._queue):
            print(item)

    def queue(self):
        """
        Returns a list of items in the queue by their priority.
        """
        return [item for _, _, item in sorted(self._queue)]

    def __len__(self):
        """
        Returns the length of the priority queue.
        """
        return len(self._queue)


class Stack:
    """
    This class implements a simple Stack data structure, based on the 'Last In First Out' mantra. It relies heavily
    on Python lists, which are ideal for implementing Stacks.

    In this program this class is utilized as a 'completed_tasks' and 'deleted_tasks' objects in the User class.
    """

    def __init__(self):
        self._items = []

    def push(self, item):
        """
        Adds a task (item) to the _items list.
        """
        self._items.append(item)

    def pop(self):
        """
        Deletes and returns the 'top' item from the _items list.
        """
        if len(self._items) == 0:
            raise IndexError('pop from empty stack')
        return self._items.pop()

    def peek(self):
        """
        Views the top task in the _items list, but does not remove or manipulate it.
        """
        if len(self._items) == 0:
            raise IndexError('peek from empty stack')
        return self._items[-1]

    def is_empty(self):
        """
        Returns 'True' if the _items list is empty
        """
        return len(self._items) == 0

    def print_stack(self):
        """
        Returns the _items list for front end display.
        """
        items_list = []
        for item in reversed(self._items):
            items_list.append(item)
        return items_list

    def __len__(self):
        """
        Provides the length of the stack.
        """
        return len(self._items)


class User:
    """
    This User class represents a user of the task manager program.

    This class stores tasks unique to the user by utilizing the PriorityQueue and Stack classes and creating objects
    of them for storing data.

    The 'to_do_tasks' attribute is a PriorityQueue object, where user tasks are saved as tuples with names,
    priority levels, and indexes.

    The 'completed_tasks' attribute is a Stack object where tasks that are completed are moved to.

    The 'deleted_tasks' attribute is a Stack object too, where deleted tasks are moved (tasks that were
    deleted before they could be completed).

    """

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
        This method adds a task to the 'to_do_tasks' PQ object.

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
                return priority, index, item

    def undo(self):
        """
        This method undoes a deletion by removing the last item added to the 'deleted_tasks' Stack object.

        1) If the length of 'deleted_tasks' is greater than 0...
        2) Unpack the last tuple stored in the 'deleted_tasks' Stack and run the pop() method on it.
        3) Add the task (name) and its priority level to the 'to_do_tasks' Stack object.
        """
        # 1
        if len(self.deleted_tasks) > 0:
            # 2
            priority, index, task = self.deleted_tasks.pop()
            # 3
            self.to_do_tasks.push(task, priority)
            return task


class GUI:
    def __init__(self, root):
        """
        This class creates the GUI for the program. It utilizes the tkinter module to create buttons, entry inputs,
        and listboxes to form the front end portion of the program.

        This first section of the class deals with laying out all the GUI's components and linking them to other
        relevant methods found within the GUI class.

        The methods implemented in this class utilize the User object's built-in methods to update data in the back end
        portion of the program.

        The various components of the GUI have comments to explain what they are and what they are linked to.
        """

        # Initialize the GUI
        self.root = root

        # Set the name and size of the window
        root.title("Task Manager")
        root.geometry('815x500')

        # Create a User object (named after me, the student!)
        self.user = User("Isaac", "Hillaker")

        # Heading Label, displaying the User's name
        self.heading_label = Label(root, text=f"{self.user.first_name}'s tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.place(x=10, y=5)

        # Instructions on how to add a new task
        self.instructions_label = Label(root,
                                        text="Type in a task then click the 'Add Task' button to add your new task.",
                                        font=("Helvetica", 12))
        self.instructions_label.place(x=10, y=45)

        # *******************
        # GET USER INPUT
        # *******************

        # Label for 'Task Name' input
        self.task_label_1 = Label(root,
                                  text="Task name:",
                                  font=("Helvetica", 12))
        self.task_label_1.place(x=10, y=70)

        # Task Name Entry (gather user input for Task NAME)
        self.task_1_entry = Entry(root, width=25)
        self.task_1_entry.place(x=10, y=95)

        # Error Label placeholder, empty and invisible by default. Displays an error message for bad input.
        self.invalid_input_label = Label(root, fg="red")
        self.invalid_input_label.place(x=175, y=150)

        # Label for 'Priority Level' input
        self.task_label_2 = Label(root,
                                  text="Task priority level (1, 2, or 3):",
                                  font=("Helvetica", 12))
        self.task_label_2.place(x=10, y=120)

        # Priority Level Entry (gather user input for task PRIORITY Level)
        self.task_2_entry = Entry(root, width=25)
        self.task_2_entry.place(x=10, y=150)

        # *******************
        # BUTTONS
        # *******************

        # ADD TASK button (calls add_task() method)
        self.add_button = Button(root, width=10, height=2, bg="green", fg="white", text="Add New",
                                 command=self.add_task)
        self.add_button.place(x=10, y=175)

        # UNDO button (calls undo_deletion() method)
        self.undo_button = Button(root, width=10, height=2, bg="yellow", fg="black", text="Undo Deletion",
                                  command=self.undo_deletion)
        self.undo_button.place(x=100, y=175)

        # COMPLETE TASK button (calls complete_task() method)
        self.complete_button = Button(root, width=10, height=2, bg="blue", fg="white", text="Complete Task",
                                      command=self.complete_task)
        self.complete_button.place(x=10, y=435)

        # DELETE TASK button (calls delete_task() method)
        self.remove_button = Button(root, width=10, height=2, bg="red", fg="white", text="Delete Task",
                                    command=self.delete_task)
        self.remove_button.place(x=100, y=435)

        # ************************
        # LISTBOXES & LABELS
        # This is where we can see the tasks we
        # have created, completed, and deleted.
        # ************************

        # TO-DO TASKS: Label & Listbox
        self.heading_label = Label(root, text="To-Do Tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.place(x=10, y=225)

        self.tasks_listbox = Listbox(root, width=50)
        self.tasks_listbox.place(x=10, y=260)

        # COMPLETED TASKS: Label and Listbox
        self.heading_label = Label(root, text="Completed Tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.place(x=500, y=5)

        self.completed_listbox = Listbox(root, width=50)
        self.completed_listbox.place(x=500, y=40)

        # DELETED TASKS: Label & Listbox
        self.heading_label = Label(root, text="Deleted Tasks", font=("Helvetica", 18, "bold"))
        self.heading_label.place(x=500, y=215)

        self.deleted_tasks_listbox = Listbox(root, width=50)
        self.deleted_tasks_listbox.place(x=500, y=250)

    # *****************
    # GUI METHODS
    # *****************

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
        3) Sort the task list by priority
        4) Loop through the sorted list and add tasks to the new listbox
        """
        # 1
        self.tasks_listbox.delete(0, END)
        # 2
        pq = self.user.to_do_tasks
        task_list = pq._queue
        # 3
        sorted_tasks = sorted(task_list, key=lambda x: x[0])
        # 4
        for _, priority, name in sorted_tasks:
            self.tasks_listbox.insert(END, name)

    def complete_task(self):
        """
        This method takes a task from the 'To-Do Listbox and moves it to the 'Completed Tasks' listbox. It also
        updates the User's 'completed_tasks' Stack object.

        1) Get the selected item from the tasks listbox, if any
        2) Add task to User object's Stack 'completed_tasks'
        3) Get the current version of 'completed_list' Stack
        4) Update 'Completed Tasks Listbox' with the current items in User's 'completed_tasks' Stack object
        5) Update the To-Do Listbox with User's current 'to_do_tasks' PQ object
        """
        # 1
        if self.tasks_listbox.curselection():
            selected_item = self.tasks_listbox.get(self.tasks_listbox.curselection())

            # 2
            self.user.complete_task(selected_item)

            # 3
            completed_tasks = self.user.completed_tasks.print_stack()

            # 4
            self.completed_listbox.delete(0, END)
            for task in completed_tasks:
                self.completed_listbox.insert(END, task)

            # 5
            self.update_listbox()

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
        """
        This method removes the last deleted task from the 'Deleted Tasks Listbox' and moves it back into the
        'To Do Tasks' listbox. It also updates the User's 'to_do_tasks' PriorityQueue object and 'deleted_tasks'
        Stack object. It then calls the update_listbox() method to update the listboxes with the most up-to-date
        information.
        """
        # Get last deleted item from User object's 'deleted_tasks' Stack
        self.user.undo()

        # Remove the last item from the deleted tasks listbox
        self.deleted_tasks_listbox.delete(self.deleted_tasks_listbox.index(END) - 1)

        # Update the To-Do listbox to make sure remaining items are ordered
        self.update_listbox()
