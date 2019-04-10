import datetime
import csv


def main_menu():
    menu_options = """
    Work Log Main Menu
    Please select from the options below?
    a) Add a new entry
    b) Search in existing entries
    c) Quit program
    """
    print(menu_options)

    while True:
        try:
            menu_selection = input("> ").lower()
            if menu_selection == "a":
                new_entry(menu_options)
            elif menu_selection == "b":
                search_entries()
            elif menu_selection == "c":
                break
            elif menu_selection != "a" or menu_selection != "b" or menu_selection != "c":
                raise ValueError
        except ValueError:
            print("You must select a valid option. (a, b, or c)")


def new_entry(menu_options):
    title = input("Title of task: ")
    while True:
        try:
            task_date = input("Enter task date. Please use DD-MM-YYYY: ")
            strp_task_date = datetime.datetime.strptime(task_date, "%d-%m-%Y")
            fmt_task_date = strp_task_date.strftime("%d-%m-%Y")
        except ValueError:
            print("You must use the following date format DD-MM-YYYY")
        else:
            while True:
                try:
                    time_spent = int(input("Time spent on task. (Rounded Minutes): "))
                except ValueError:
                    print("You must use rounded minutes. example: 12 ")
                else:
                    break
            break
    optional_notes = input("Optional notes. (You may leave this blank): ")
    write_to_file(title, fmt_task_date, time_spent, optional_notes)
    print("Your entry has been recorded.")
    print(menu_options)


def write_to_file(title, fmt_task_date, time_spent, optional_notes):
    with open("work_log.csv", "a", newline="") as csvfile:
        fieldnames = ["Title", "Task Date", "Time", "Notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({
                        "Title": title,
                        "Task Date": fmt_task_date,
                        "Time": time_spent,
                        "Notes": optional_notes
                        })


def search_entries():
    pass


if __name__ == "__main__":
    with open("work_log.csv", "w", newline="") as csvfile:
        fieldnames = ["Title", "Task Date", "Time", "Notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    main_menu()
