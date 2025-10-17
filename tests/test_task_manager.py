import unittest
import os
import json
from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    TASK_FILE = "test_tasks.json"

    def setUp(self):
        # Create a new TaskManager instance with a temporary task file
        self.task_manager = TaskManager(self.TASK_FILE)
        # Ensure the task list is empty before each test
        self.task_manager.tasks = []
        self.task_manager.save_tasks()

    def tearDown(self):
        # Clean up the temporary task file after each test
        if os.path.exists(self.TASK_FILE):
            os.remove(self.TASK_FILE)

    def test_add_task(self):
        self.task_manager.add_task("Test task")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Test task")
        self.assertEqual(tasks[0]["completed"], False)
        self.assertEqual(tasks[0]["id"], 1)

    def test_list_tasks(self):
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["description"], "Task 1")
        self.assertEqual(tasks[1]["description"], "Task 2")

    def test_complete_task(self):
        self.task_manager.add_task("Task to complete")
        self.task_manager.complete_task(1)
        tasks = self.task_manager.list_tasks()
        self.assertEqual(tasks[0]["completed"], True)

    def test_complete_task_not_found(self):
        with self.assertRaises(ValueError):
            self.task_manager.complete_task(1)

    def test_delete_task(self):
        self.task_manager.add_task("Task to delete")
        self.task_manager.delete_task(1)
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_task_not_found(self):
        with self.assertRaises(ValueError):
            self.task_manager.delete_task(1)

    def test_load_tasks_from_file(self):
        # Create a task file with initial data
        initial_tasks = [{"id": 1, "description": "Initial Task", "completed": False}]
        with open(self.TASK_FILE, "w") as f:
            json.dump(initial_tasks, f)

        task_manager = TaskManager(self.TASK_FILE)  # Load from the created file
        tasks = task_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Initial Task")

    def test_load_tasks_empty_file(self):
        # Create an empty task file
        open(self.TASK_FILE, 'w').close()
        task_manager = TaskManager(self.TASK_FILE)
        tasks = task_manager.list_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()