import os

# Define the file name for storing tasks
TASKS_FILE = "tasks.txt"

def load_tasks():
    """Loads tasks from the file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        # Read lines and strip trailing newline characters
        tasks = [line.strip() for line in f.readlines()]
    return tasks

def save_tasks(tasks):
    """Saves tasks to the file."""
    with open(TASKS_FILE, 'w') as f:
        for task in tasks:
            f.write(task + "\n")

def add_task(tasks, task_description):
    """Adds a new task."""
    tasks.append(task_description)
    save_tasks(tasks)
    print(f"Added task: '{task_description}'")

def view_tasks(tasks):
    """Prints all tasks with their index."""
    if not tasks:
        print("Your To-Do list is empty!")
        return

    print("\n📝 Current To-Do List:")
    for i, task in enumerate(tasks):
        # Format: [Index]. Task Description
        print(f"  {i+1}. {task}")
    print("-" * 30)

def delete_task(tasks, task_index):
    """Deletes a task by its 1-based index."""
    try:
        # Convert to 0-based index
        index = int(task_index) - 1
        if 0 <= index < len(tasks):
            removed_task = tasks.pop(index)
            save_tasks(tasks)
            print(f"Deleted task: '{removed_task}'")
        else:
            print(f"Error: Invalid task number {task_index}")
    except ValueError:
        print("Error: Task number must be an integer.")

def main():
    """Main function to run the CLI application."""
    tasks = load_tasks()

    while True:
        print("\n*** To-Do CLI Menu ***")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            new_task = input("Enter the task description: ").strip()
            if new_task:
                add_task(tasks, new_task)
            else:
                print("Task description cannot be empty.")
        elif choice == '3':
            view_tasks(tasks)
            if tasks:
                task_num = input("Enter the number of the task to delete: ")
                delete_task(tasks, task_num)
        elif choice == '4':
            print("Exiting To-Do CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    # Clean up the previous tasks file for a clean start in this run
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    main()
