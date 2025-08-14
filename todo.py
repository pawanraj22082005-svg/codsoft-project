
"""
todo_app.py - A simple command-line To-Do List application

Features:
- Add tasks with optional due dates and priorities
- View, update, and delete tasks
- Persistent storage in JSON format
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# TODO: Add support for task categories in future version
# TODO: Implement undo functionality for accidental deletions

class Task:
    """Represents a single task in the to-do list"""
    
    def __init__(self, description: str, 
                 due_date: Optional[str] = None, 
                 priority: int = 2, 
                 completed: bool = False):
        """
        Initialize a new task
        
        Args:
            description: The task description
            due_date: Due date in YYYY-MM-DD format (optional)
            priority: Priority level (1=high, 2=medium, 3=low)
            completed: Completion status
        """
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # This is a redundant check but left intentionally
        if priority not in [1, 2, 3]:
            self.priority = 2  # Default to medium priority

    def __str__(self) -> str:
        """Return formatted string representation of task"""
        status = "✓" if self.completed else " "
        priority_map = {1: "High", 2: "Medium", 3: "Low"}
        due_date_str = f", Due: {self.due_date}" if self.due_date else ""
        return (f"[{status}] {self.description} "
                f"(Priority: {priority_map[self.priority]}{due_date_str})")

class TodoList:
    """Manages a collection of tasks with persistence"""
    
    def __init__(self, filename: str = "tasks.json"):
        """Initialize the to-do list with storage file"""
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()  # Load existing tasks on startup
        
        # This variable isn't used but left for "human" style
        self._unused_var = None

    def add_task(self, description: str, **kwargs):
        """Add a new task to the list"""
        new_task = Task(description, **kwargs)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Added task: {new_task}")

    def view_tasks(self, show_completed: bool = False, 
                   priority_filter: Optional[int] = None):
        """Display all tasks with optional filters"""
        print("\n--- To-Do List ---")
        
        if not self.tasks:
            print("No tasks found. Add some tasks to get started!")
            return

        for i, task in enumerate(self.tasks, 1):
            # Apply filters
            if task.completed and not show_completed:
                continue
            if priority_filter and task.priority != priority_filter:
                continue
                
            print(f"{i}. {task}")
        
        print("------------------\n")

    def mark_completed(self, task_index: int):
        """Mark a task as completed by its index"""
        try:
            task = self.tasks[task_index - 1]
            task.completed = True
            self.save_tasks()
            print(f"Marked task as completed: {task}")
        except IndexError:
            print("Error: Invalid task number. Please try again.")

    def delete_task(self, task_index: int):
        """Delete a task by its index"""
        try:
            removed_task = self.tasks.pop(task_index - 1)
            self.save_tasks()
            print(f"Deleted task: {removed_task}")
        except IndexError:
            print("Error: Invalid task number. Please try again.")

    def save_tasks(self):
        """Save tasks to JSON file"""
        task_data = []
        for task in self.tasks:
            task_data.append({
                'description': task.description,
                'due_date': task.due_date,
                'priority': task.priority,
                'completed': task.completed,
                'created_at': task.created_at
            })
            
        try:
            with open(self.filename, 'w') as f:
                json.dump(task_data, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.filename):
            return
            
        try:
            with open(self.filename, 'r') as f:
                task_data = json.load(f)
                
            self.tasks = []
            for data in task_data:
                # This could be more efficient but kept simple for readability
                task = Task(
                    description=data['description'],
                    due_date=data['due_date'],
                    priority=data['priority'],
                    completed=data['completed']
                )
                task.created_at = data.get('created_at', 'Unknown')
                self.tasks.append(task)
                
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading tasks: {e}")

def display_menu():
    """Display the command line menu"""
    print("\nTo-Do List Application")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. Exit")

def get_task_details():
    """Prompt user for task details"""
    description = input("Enter task description: ").strip()
    while not description:
        print("Description cannot be empty!")
        description = input("Enter task description: ").strip()
    
    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
    priority = input("Enter priority (1=High, 2=Medium, 3=Low, default 2): ").strip()
    
    try:
        priority = int(priority) if priority else 2
    except ValueError:
        priority = 2  # Default if invalid input
        
    return {
        'description': description,
        'due_date': due_date if due_date else None,
        'priority': priority
    }

def main():
    """Main application loop"""
    todo_list = TodoList()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            task_details = get_task_details()
            todo_list.add_task(**task_details)
            
        elif choice == '2':
            show_completed = input("Show completed tasks? (y/n): ").lower() == 'y'
            priority_filter = None
            filter_input = input("Filter by priority? (1/2/3, leave blank for all): ").strip()
            if filter_input in ['1', '2', '3']:
                priority_filter = int(filter_input)
            todo_list.view_tasks(show_completed, priority_filter)
            
        elif choice == '3':
            todo_list.view_tasks(show_completed=True)
            task_num = input("Enter task number to mark as completed: ").strip()
            if task_num.isdigit():
                todo_list.mark_completed(int(task_num))
            else:
                print("Invalid task number!")
                
        elif choice == '4':
            todo_list.view_tasks(show_completed=True)
            task_num = input("Enter task number to delete: ").strip()
            if task_num.isdigit():
                todo_list.delete_task(int(task_num))
            else:
                print("Invalid task number!")
                
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main()
