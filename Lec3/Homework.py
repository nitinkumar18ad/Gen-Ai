import json
import os

# File to store data
FILE_NAME = "students.json"

# Load data from file
def load_students():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

# edit 
def edit_student(students, index, new_name, new_marks):
    if 0 <= index < len(students):
        students[index]["name"] = new_name
        students[index]["marks"] = new_marks
        save_students(students)
        print(f"✏️ Student updated to '{new_name}' with {new_marks} marks!")
    else:
        print("⚠️ Invalid student number.")

# Save data to file
def save_students(students):
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)

# Show help
def show_help():
    print("""
📌 Commands:
add <name> <marks>  -> Add student
view                -> View all students
delete <number>     -> Delete student
edit <number> <name> <marks> -> Edit student
search <name>       -> Search student
help                -> Show commands
exit                -> Exit bot
""")

# Add student
def add_student(students, name, marks):
    students.append({"name": name, "marks": marks})
    save_students(students)
    print(f"✅ Student '{name}' added with {marks} marks!")

# View students
def view_students(students):
    if not students:
        print("📭 No students found.")
        return

    print("\n📋 Student List:")
    for i, student in enumerate(students):
        print(f"{i+1}. {student['name']} - {student['marks']} marks")

# Delete student
def delete_student(students, index):
    if 0 <= index < len(students):
        removed = students.pop(index)
        save_students(students)
        print(f"❌ '{removed['name']}' deleted.")
    else:
        print("⚠️ Invalid student number.")

# Search student
def search_student(students, name):
    found = False
    for student in students:
        if name.lower() in student["name"].lower():
            print(f"🔍 Found: {student['name']} - {student['marks']} marks")
            found = True
    if not found:
        print("❌ No matching student found.")

# Chatbot response handler
def handle_input(user_input, students):
    parts = user_input.strip().split()

    if not parts:
        return students

    command = parts[0].lower()

    if command == "help":
        show_help()

    elif command == "view":
        view_students(students)

    elif command == "add":
        if len(parts) >= 3:
            name = parts[1]
            try:
                marks = int(parts[2])
                add_student(students, name, marks)
            except:
                print("⚠️ Marks should be a number.")
        else:
            print("⚠️ Usage: add <name> <marks>")

    elif command == "delete":
        if len(parts) >= 2:
            try:
                index = int(parts[1]) - 1
                delete_student(students, index)
            except:
                print("⚠️ Enter a valid number.")
        else:
            print("⚠️ Usage: delete <number>")

    elif command == "search":
        if len(parts) >= 2:
            name = parts[1]
            search_student(students, name)
        else:
            print("⚠️ Usage: search <name>")

    elif command == "edit":
        if len(parts) >= 4:
            try:
                index = int(parts[1]) - 1
                new_name = parts[2]
                new_marks = int(parts[3])
                edit_student(students, index, new_name, new_marks)
            except:
                print("⚠️ Usage: edit <number> <name> <marks>")
        else:
            print("⚠️ Usage: edit <number> <name> <marks>")
            

    else:
        print("🤖 Bot: I didn't understand that. Type 'help'.")

    

    return students

# Main chatbot loop
def chatbot():
    students = load_students()

    print("🤖 Student Manager Chatbot")
    print("Type 'help' to see commands.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        students = handle_input(user_input, students)

# Run chatbot
if __name__ == "__main__":
    chatbot()