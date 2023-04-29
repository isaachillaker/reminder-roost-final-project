"""
AUTHOR: Isaac Hillaker
ASSIGNMENT: Final Project: Task Manager
DATE: 04/28/2023
INFO:

    These unit tests test the four classes and their methods, found in rr_classes.py. The rr_classes.py file is
    found in the same directory as these unit tests.

I completed this assignment without any unauthorized assistance.
"""

import unittest
from unittest.mock import patch
from tkinter import Tk, END
from rr_classes import User, PriorityQueue, Stack, GUI


class TestUser(unittest.TestCase):

    def test_init(self):
        user = User('Alice', 'Applebaum')
        self.assertEqual(user.first_name, 'Alice')
        self.assertEqual(user.last_name, 'Applebaum')
        self.assertIsInstance(user.to_do_tasks, PriorityQueue)
        self.assertIsInstance(user.completed_tasks, Stack)
        self.assertIsInstance(user.deleted_tasks, Stack)

    def test_get_valid_name(self):
        with patch('builtins.input', return_value='Alice Applebaum'):
            user = User()
            name = user.get_valid_name("Enter a name: ")
            self.assertEqual(name, 'Alice Applebaum')

    def test_validate_name(self):
        user = User("Alice", "Applebaum")
        self.assertRaises(ValueError, user.validate_name, "123")
        self.assertRaises(ValueError, user.validate_name, "Alice123")
        self.assertRaises(ValueError, user.validate_name, "Alice?")
        self.assertEqual(user.validate_name("Alice"), "Alice")
        self.assertEqual(user.validate_name("Alice-Applebaum"), "Alice-Applebaum")
        self.assertEqual(user.validate_name("Alice O'Neil"), "Alice O'Neil")

    def test_add_task(self):
        user = User("Alice", "Applebaum")
        self.assertEqual(user.add_task(), "Both task and priority must be specified!")
        self.assertEqual(user.add_task("task1"), "Both task and priority must be specified!")
        self.assertEqual(user.add_task(priority=1), "Both task and priority must be specified!")
        self.assertIsNone(user.add_task("task1", 1))

    def test_complete_task(self):
        user = User("Alice", "Applebaum")
        self.assertIsNone(user.complete_task())
        self.assertIsNone(user.complete_task("task1"))
        user.add_task("task1", 1)
        user.add_task("task2", 2)
        self.assertEqual(user.complete_task(), "task2")
        self.assertEqual(user.completed_tasks.peek(), "task2")
        self.assertEqual(user.complete_task("task1"), "task1")
        self.assertEqual(user.completed_tasks.peek(), "task1")

    def test_delete_task(self):
        user = User("Alice", "Applebaum")
        self.assertIsNone(user.delete_task("task1"))
        user.add_task("task1", 1)
        self.assertEqual(user.delete_task("task1"), (-1, 0, "task1"))
        self.assertEqual(user.deleted_tasks.peek(), (1, 0, "task1"))

    def test_undo(self):
        user = User("Alice", "Applebaum")
        self.assertIsNone(user.undo())
        user.add_task("task1", 1)
        user.add_task("task2", 2)
        user.delete_task("task1")
        self.assertEqual(user.undo(), "task1")


class TestPriorityQueue(unittest.TestCase):
    def test_push_and_pop(self):
        queue = PriorityQueue()
        queue.push("item1", 2)
        queue.push("item2", 1)
        queue.push("item3", 3)
        self.assertEqual(queue.pop(), "item3")
        self.assertEqual(queue.pop(), "item1")
        self.assertEqual(queue.pop(), "item2")
        self.assertEqual(len(queue), 0)

    def test_len(self):
        queue = PriorityQueue()
        self.assertEqual(len(queue), 0)
        queue.push("item1", 1)
        self.assertEqual(len(queue), 1)
        queue.push("item2", 2)
        self.assertEqual(len(queue), 2)
        queue.pop()
        self.assertEqual(len(queue), 1)

    def test_print_queue(self):
        queue = PriorityQueue()
        queue.push("item1", 1)
        queue.push("item2", 2)
        queue.push("item3", 3)
        queue.push("item4", 2)
        queue.push("item5", 1)
        queue.push("item6", 3)
        queue.push("item7", 3)

        expected_output = "item3\nitem6\nitem7\nitem2\nitem4\nitem1\nitem5\n"
        self.assertEqual('\n'.join(queue.queue()), expected_output.strip())

    def test_queue(self):
        queue = PriorityQueue()
        queue.push("item1", 1)
        queue.push("item2", 2)
        queue.push("item3", 3)
        queue.push("item4", 2)
        queue.push("item5", 1)
        queue.push("item6", 3)
        queue.push("item7", 3)
        self.assertEqual(queue.queue(), ["item3", "item6", "item7", "item2", "item4", "item1", "item5"])


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())
        self.assertRaises(IndexError, s.pop)

    def test_peek(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.peek(), 3)
        s.pop()
        self.assertEqual(s.peek(), 2)
        s.pop()
        self.assertEqual(s.peek(), 1)
        s.pop()
        self.assertRaises(IndexError, s.peek)

    def test_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())
        s.pop()
        self.assertTrue(s.is_empty())

    def test_print_stack(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.print_stack(), [3, 2, 1])
        s.pop()
        self.assertEqual(s.print_stack(), [2, 1])
        s.pop()
        self.assertEqual(s.print_stack(), [1])
        s.pop()
        self.assertEqual(s.print_stack(), [])
        self.assertTrue(s.is_empty())

    def test_len(self):
        s = Stack()
        self.assertEqual(len(s), 0)
        s.push(1)
        self.assertEqual(len(s), 1)
        s.push(2)
        self.assertEqual(len(s), 2)
        s.push(3)
        self.assertEqual(len(s), 3)
        s.pop()
        self.assertEqual(len(s), 2)
        s.pop()
        self.assertEqual(len(s), 1)
        s.pop()
        self.assertEqual(len(s), 0)
        self.assertTrue(s.is_empty())
        self.assertRaises(IndexError, s.pop)


class TestGUI(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.gui = GUI(self.root)
        self.gui.task_1_entry.insert(0, "Walk the dog")
        self.gui.task_2_entry.insert(0, "1")

    def test_add_task_valid_input(self):
        self.gui.add_task()
        self.assertEqual(self.gui.tasks_listbox.get(END), "Walk the dog")
        self.assertEqual(self.gui.task_1_entry.get(), "")
        self.assertEqual(self.gui.task_2_entry.get(), "")

    def test_add_task_invalid_priority(self):
        self.gui.task_2_entry.delete(0, END)
        self.gui.task_2_entry.insert(0, "4")
        self.gui.add_task()
        self.assertEqual(self.gui.invalid_input_label.cget("text"), "Number out of range. Must be a 1, 2, or 3!")
        self.assertEqual(self.gui.task_1_entry.get(), "Walk the dog")
        self.assertEqual(self.gui.task_2_entry.get(), "4")

    def test_add_task_invalid_input(self):
        self.gui.task_2_entry.delete(0, END)
        self.gui.task_2_entry.insert(0, "a")
        self.gui.add_task()
        self.assertEqual(self.gui.invalid_input_label.cget("text"), "Must be a number: 1, 2, or 3!")
        self.assertEqual(self.gui.task_1_entry.get(), "Walk the dog")
        self.assertEqual(self.gui.task_2_entry.get(), "a")

    def test_update_listbox(self):
        self.gui.add_task()
        self.gui.task_1_entry.insert(0, "Buy groceries")
        self.gui.task_2_entry.insert(0, "2")
        self.gui.add_task()
        expected_list = ["Buy groceries", "Walk the dog"]
        self.assertEqual(list(self.gui.tasks_listbox.get(0, END)), expected_list)

    def test_complete_task(self):
        self.gui.add_task()
        self.gui.complete_task()
        self.assertEqual(list(self.gui.completed_listbox.get(0, END)), [])
        self.assertEqual(list(self.gui.tasks_listbox.get(0, END)), ['Walk the dog'])

    def test_delete_task(self):
        self.gui.add_task()
        self.gui.task_1_entry.insert(0, "Buy groceries")
        self.gui.task_2_entry.insert(0, "2")
        self.gui.add_task()
        self.gui.tasks_listbox.selection_clear(0, END)
        self.gui.tasks_listbox.select_set(0)
        self.gui.delete_task()
        expected_tasks_list = ["Buy groceries"]
        expected_deleted_list = ["Walk the dog"]
        self.assertEqual(list(self.gui.tasks_listbox.get(0, END)), expected_deleted_list)
        self.assertEqual(list(self.gui.deleted_tasks_listbox.get(0, END)), expected_tasks_list)

    def test_undo_deletion(self):
        self.gui.add_task()
        self.gui.task_1_entry.insert(0, "Buy groceries")
        self.gui.task_2_entry.insert(0, "2")
        self.gui.add_task()
        self.gui.tasks_listbox.selection_clear(0, END)
        self.gui.tasks_listbox.select_set(0)
        self.gui.delete_task()
        self.gui.undo_deletion()
        expected_tasks_list = ["Buy groceries", "Walk the dog"]
        expected_deleted_list = []
        self.assertEqual(list(self.gui.tasks_listbox.get(0, END)), expected_tasks_list)
