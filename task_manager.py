# Minor edit
import json
import os

class TaskManager:
    def __init__(self, task_file):
        self.task_file = task_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        else:
            return []

    def save_tasks(self):
        with open(self.task_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, description):
        new_task = {
            "id": self.get_next_id(),
            "description": description,
            "completed": False,
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def complete_task(self, task_id):
        task_id = int(task_id)
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return
        raise ValueError(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        task_id = int(task_id)
        original_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(self.tasks) < original_length:
           self.save_tasks()
           return

        raise ValueError(f"Task with ID {task_id} not found.")

    def get_next_id(self):
        if not self.tasks:
            return 1
        else:
            return max(task["id"] for task in self.tasks) + 1