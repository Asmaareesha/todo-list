import json
import os
from datetime import date, datetime

os.system("")  # makes colors work in the Windows terminal

FILENAME = "tasks.json"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GREY = "\033[90m"
RESET = "\033[0m"

PRIORITY_COLORS = {"High": RED, "Medium": YELLOW, "Low": GREEN}


# ---------- Saving and loading ----------

def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file)


# ---------- Asking the user for input ----------

def ask_number(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a number.")
        return None


def ask_priority(editing=False):
    prompt = "Priority (1 = High, 2 = Medium, 3 = Low)"
    if editing:
        prompt += ", or press Enter to keep"
    prompt += ": "
    while True:
        answer = input(prompt)
        if answer == "" and editing:
            return "KEEP"
        if answer == "1":
            return "High"
        if answer == "2":
            return "Medium"
        if answer == "3":
            return "Low"
        print("Please type 1, 2, or 3.")


def ask_due_date(editing=False):
    if editing:
        prompt = "Due date (YYYY-MM-DD), Enter to keep, or 'none' to remove: "
    else:
        prompt = "Due date (YYYY-MM-DD) or press Enter to skip: "
    while True:
        answer = input(prompt).strip()
        if answer == "":
            return "KEEP" if editing else None
        if answer.lower() == "none" and editing:
            return None
        try:
            datetime.strptime(answer, "%Y-%m-%d")
            return answer
        except ValueError:
            print("Please use the format YYYY-MM-DD, like 2026-12-31.")


# ---------- Showing tasks ----------

def is_overdue(task):
    due = task.get("due")
    if task["done"] or not due:
        return False
    return datetime.strptime(due, "%Y-%m-%d").date() < date.today()


def format_task(number, task):
    mark = "✓" if task["done"] else " "
    priority = task.get("priority", "Medium")
    text = f"{number}. [{mark}] {task['title']} ({priority})"

    due = task.get("due")
    if due:
        text += f" - due {due}"

    if task["done"]:
        return f"{GREY}{text}{RESET}"
    if is_overdue(task):
        return f"{MAGENTA}{text} - OVERDUE!{RESET}"
    return f"{PRIORITY_COLORS[priority]}{text}{RESET}"


def show_tasks(tasks, indexes=None):
    if len(tasks) == 0:
        print("No tasks yet.")
        return

    if indexes is None:
        indexes = range(len(tasks))

    for i in indexes:
        print(format_task(i + 1, tasks[i]))

    done_count = sum(1 for task in tasks if task["done"])
    overdue_count = sum(1 for task in tasks if is_overdue(task))
    print(f"\n{done_count} of {len(tasks)} tasks completed")
    if overdue_count > 0:
        print(f"{MAGENTA}{overdue_count} overdue{RESET}")


def show_menu():
    print(f"\n{CYAN}=== TO-DO LIST ==={RESET}")
    print("1. Add task")
    print("2. View tasks")
    print("3. Edit task")
    print("4. Complete task")
    print("5. Delete task")
    print("6. Search tasks")
    print("7. Quit")


# ---------- Main program ----------

tasks = load_tasks()

while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        title = input("Enter a task: ")
        priority = ask_priority()
        due = ask_due_date()
        tasks.append({"title": title, "done": False,
                      "priority": priority, "due": due})
        save_tasks(tasks)
        print(f"{GREEN}Task added!{RESET}")

    elif choice == "2":
        show_tasks(tasks)

    elif choice == "3":
        number = ask_number("Task number to edit: ")
        if number is None:
            continue
        if 1 <= number <= len(tasks):
            task = tasks[number - 1]
            print(f"Editing: {task['title']}")

            new_title = input("New title (press Enter to keep): ")
            if new_title != "":
                task["title"] = new_title

            new_priority = ask_priority(editing=True)
            if new_priority != "KEEP":
                task["priority"] = new_priority

            new_due = ask_due_date(editing=True)
            if new_due != "KEEP":
                task["due"] = new_due

            save_tasks(tasks)
            print(f"{GREEN}Task updated!{RESET}")
        else:
            print("No task with that number.")

    elif choice == "4":
        number = ask_number("Task number to complete: ")
        if number is None:
            continue
        if 1 <= number <= len(tasks):
            tasks[number - 1]["done"] = True
            save_tasks(tasks)
            print(f"{GREEN}Task completed!{RESET}")
        else:
            print("No task with that number.")

    elif choice == "5":
        number = ask_number("Task number to delete: ")
        if number is None:
            continue
        if 1 <= number <= len(tasks):
            removed = tasks.pop(number - 1)
            save_tasks(tasks)
            print(f"{RED}Deleted: {removed['title']}{RESET}")
        else:
            print("No task with that number.")

    elif choice == "6":
        keyword = input("Search for: ").lower()
        matches = [i for i, task in enumerate(tasks)
                   if keyword in task["title"].lower()]
        if len(matches) == 0:
            print("No matching tasks.")
        else:
            show_tasks(tasks, matches)

    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid choice, try again.")
