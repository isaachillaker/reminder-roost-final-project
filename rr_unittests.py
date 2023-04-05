from io import StringIO
from unittest.mock import patch

from rr_classes import User, PriorityQueue, Stack
import unittest
import sys


class UserTestCase(unittest.TestCase):
    def test_create_user(self):
        user = User('John', 'Doe')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(len(user.to_do_tasks), 0)
        self.assertEqual(len(user.completed_tasks), 0)

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

    def test_delete_task(self):
        user = User("Bob", "Smith")
        user.add_task("Task 1", 2)
        user.add_task("Task 2", 3)
        user.add_task("Task 3", 1)
        # Delete 'task 1' and ensure that the length of 'to_do_tasks' changed too
        self.assertEqual(user.delete_task("Task 1"), "Task 1")
        self.assertEqual(len(user.to_do_tasks), 2)
        # Ensure that length of 'deleted_tasks' is 1, because there should be 1 task in it
        self.assertEqual(len(user.deleted_tasks), 1)

    def test_undo(self):
        user = User("Bob", 'Smith')
        user.add_task("Task 1", 2)
        user.add_task("Task 2", 1)
        user.add_task("Task 3", 3)

        # Delete 'Task 3' and 'Task 2'
        user.delete_task("Task 3")
        user.delete_task("Task 2")

        # Ensure that both tasks are moved into 'deleted_tasks'
        self.assertEqual(len(user.deleted_tasks), 2)

        # Undo Deletion, removing 'Task 2'
        self.assertEqual(user.undo(), "Task 2")

        # Check that one task remains in 'deleted_tasks'
        self.assertEqual(len(user.deleted_tasks), 1)


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


class TestStack(unittest.TestCase):
    def test_push_and_pop(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)

    def test_peek(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.peek(), 3)
        stack.pop()
        self.assertEqual(stack.peek(), 2)

    def test_is_empty(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())
        stack.push(1)
        self.assertFalse(stack.is_empty())
        stack.pop()
        self.assertTrue(stack.is_empty())

    def test_print_stack(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        with unittest.mock.patch('builtins.print') as mock_print:
            stack.print_stack()
            mock_print.assert_has_calls([
                unittest.mock.call(3),
                unittest.mock.call(2),
                unittest.mock.call(1)
            ])

    def test_pop_empty_stack(self):
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.pop()

    def test_peek_empty_stack(self):
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.peek()


if __name__ == '__main__':
    unittest.main()
