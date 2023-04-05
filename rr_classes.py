import heapq, re


class User:
    def __init__(self, first_name, last_name):
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.to_do_tasks = PriorityQueue()

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
        return self.to_do_tasks.pop()


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def __len__(self):
        return len(self._queue)


