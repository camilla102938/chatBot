def display_checklist(checklist):
    print("\nChecklist:")
    for index, item in enumerate(checklist, start=1):
        status = "[x]" if item['completed'] else "[ ]"
        print(f"{index}. {status} {item['task']}")

def add_item(checklist, task):
    checklist.append({"task": task, "completed": False})

def mark_completed(checklist, index):
    if 0 <= index < len(checklist):
        checklist[index]['completed'] = True

def remove_item(checklist, index):
    if 0 <= index < len(checklist):
        checklist.pop(index)

# Main program
checklist = []
while True:
    display_checklist(checklist)
    print("\nOptions:")
    print("1. Add item")
    print("2. Mark item as completed")
    print("3. Remove item")
    print("4. Quit")

    choice = input("Choose an option: ")
    
    if choice == "1":
        task = input("Enter the task: ")
        add_item(checklist, task)
    elif choice == "2":
        index = int(input("Enter the task number to mark as completed: ")) - 1
        mark_completed(checklist, index)
    elif choice == "3":
        index = int(input("Enter the task number to remove: ")) - 1
        remove_item(checklist, index)
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")

print("Goodbye!")