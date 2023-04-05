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

    def get_valid_name(self, name):
        while True:
            name = input(f"{name}")
            try:
                validated_name = self.validate_name(name)
                return validated_name
            except ValueError as e:
                print(e)

    def validate_name(self, name):
        # Check that the name contains only letters and allowed symbols
        if not re.match(r'^[A-Za-z\'\- ]+$', name):
            raise ValueError('Invalid name: only letters, "-" and "\'" allowed')
        return name.strip()

    def add_task(self, task, priority):
        self.to_do_tasks.push(task, priority)

    def complete_task(self):
        if len(self.to_do_tasks) == 0:
            return None
        completed_task = self.to_do_tasks.pop()
        self.completed_tasks.push(completed_task)
        return completed_task


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
