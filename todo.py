import json

FILENAME = "tasks.json"


def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file)


tasks = load_tasks()

while True:
    print("\n1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Complete task")
    print("5. Quit")
    choice = input("Choose an option: ")

    if choice == "1":
        task = input("Enter a task: ")
        tasks.append({"title": task, "done": False})
        save_tasks(tasks)
        print("Task added!")

    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks yet.")
        else:
            for number, task in enumerate(tasks, start=1):
                mark = "✓" if task["done"] else " "
                print(f"{number}. [{mark}] {task['title']}")

    elif choice == "3":
        try:
            number = int(input("Task number to delete: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if 1 <= number <= len(tasks):
            removed = tasks.pop(number - 1)
            save_tasks(tasks)
            print(f"Deleted: {removed['title']}")
        else:
            print("No task with that number.")

    elif choice == "4":
        try:
            number = int(input("Task number to complete: "))
        except ValueError:
            print("Please enter a number.")
            continue
        if 1 <= number <= len(tasks):
            tasks[number - 1]["done"] = True
            save_tasks(tasks)
            print("Task completed!")
        else:
            print("No task with that number.")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice, try again.")
