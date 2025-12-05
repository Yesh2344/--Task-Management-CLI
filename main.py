import argparse
import json
import os
from colorama import Fore, Style, init

from task_manager import TaskManager

# Initialize colorama for cross-platform color support
init()

TASK_FILE = "tasks.json"


def main():
    task_manager = TaskManager(TASK_FILE)

    parser = argparse.ArgumentParser(description="Task Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="Task ID to complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    if args.command == "add":
        task_manager.add_task(args.description)
        print(Fore.GREEN + "Task added successfully!" + Style.RESET_ALL)
    elif args.command == "list":
        tasks = task_manager.list_tasks()
        if not tasks:
            print(Fore.YELLOW + "No tasks found." + Style.RESET_ALL)
        else:
            for task in tasks:
                status_color = Fore.GREEN if task["completed"] else Fore.RED
                print(
                    f"{Fore.CYAN}ID:{Style.RESET_ALL} {task['id']}, {Fore.BLUE}Description:{Style.RESET_ALL} {task['description']}, {Fore.MAGENTA}Status:{Style.RESET_ALL} {status_color}{task['completed']}{Style.RESET_ALL}"
                )
    elif args.command == "complete":
        try:
            task_manager.complete_task(args.task_id)
            print(Fore.GREEN + "Task marked as complete!" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
    elif args.command == "delete":
        try:
            task_manager.delete_task(args.task_id)
# Added comment
            print(Fore.GREEN + "Task deleted successfully!" + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()