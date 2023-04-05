from io import StringIO
from unittest.mock import patch

from rr_classes import User, PriorityQueue
import unittest
import sys


class UserTestCase(unittest.TestCase):
    def test_create_user(self):
        user = User('John', 'Doe')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(len(user.to_do_tasks), 0)
        self.assertEqual(len(user.completed_tasks), 0)

    def test_create_user_with_invalid_name(self):
        with self.assertRaises(ValueError):
            User('John1', 'Doe')

    def test_add_task(self):
        user = User('John', 'Doe')
        user.add_task('Task 1', 1)
        user.add_task('Task 2', 2)
        self.assertEqual(len(user.to_do_tasks), 2)

    def test_complete_task(self):
        user = User('John', 'Doe')
        user.add_task('Task 1', 1)
        user.add_task('Task 2', 2)
        completed_task = user.complete_task()
        self.assertEqual(completed_task, 'Task 2')
        self.assertEqual(len(user.to_do_tasks), 1)
        self.assertEqual(len(user.completed_tasks), 1)
        completed_task = user.complete_task()
        self.assertEqual(completed_task, 'Task 1')
        self.assertEqual(len(user.to_do_tasks), 0)
        self.assertEqual(len(user.completed_tasks), 2)

    def test_complete_task_no_tasks(self):
        user = User('John', 'Doe')
        completed_task = user.complete_task()
        self.assertIsNone(completed_task)


class TestPriorityQueue(unittest.TestCase):
    def test_push(self):
        q = PriorityQueue()
        q.push('task 1', 1)
        q.push('task 2', 2)
        q.push('task 3', 3)
        self.assertEqual(len(q), 3)

    def test_pop(self):
        q = PriorityQueue()
        q.push('task 1', 1)
        q.push('task 2', 2)
        q.push('task 3', 3)
        self.assertEqual(q.pop(), 'task 3')
        self.assertEqual(q.pop(), 'task 2')
        self.assertEqual(q.pop(), 'task 1')
        self.assertEqual(len(q), 0)

    def test_print_queue(self):
        pq = PriorityQueue()
        pq.push('task 1', 1)
        pq.push('task 2', 2)
        pq.push('task 3', 3)
        expected_output = "task 3\ntask 2\ntask 1\n"
        with patch('sys.stdout', new=StringIO()) as output:
            pq.print_queue()
            self.assertEqual(output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()

