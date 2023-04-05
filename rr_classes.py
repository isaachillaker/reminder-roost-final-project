import heapq, re


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
                self.deleted_tasks.push(item)
                return item

    def undo(self):
        """
        This method removes the last item added to the 'deleted_tasks' Stack object and returns it
        to the 'to_do_tasks' PQ object.
        """
        if len(self.deleted_tasks) == 0:
            return None

        if len(self.deleted_tasks) > 0:
            task = self.deleted_tasks.pop()
            priority = self.to_do_tasks._queue[0][0]
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
