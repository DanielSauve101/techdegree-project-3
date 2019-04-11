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
                search_menu(menu_options)
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
                    fmt_time_spent = datetime.timedelta(minutes=time_spent)
                except ValueError:
                    print("You must use rounded minutes. example: 12 ")
                else:
                    print(fmt_time_spent)
                    break
            break
    optional_notes = input("Optional notes. (You may leave this blank): ")
    write_to_file(title, fmt_task_date, fmt_time_spent, optional_notes)
    print("Your entry has been recorded.")
    print(menu_options)


def write_to_file(title, fmt_task_date, fmt_time_spent, optional_notes):
    with open("work_log.csv", "a", newline="") as csvfile:
        fieldnames = ["Title", "Task Date", "Time", "Notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({
                        "Title": title,
                        "Task Date": fmt_task_date,
                        "Time": fmt_time_spent,
                        "Notes": optional_notes
                        })


def search_menu(menu_options):
    print("""
    Search Menu
    Please select from the options below?
    a) Search by date
    b) Search by time spent
    c) Search by exact title
    d) Search by regex
    e) Previous menu
    """)
    while True:
        try:
            search_selection = input("> ").lower()
            if search_selection == "a":
                search_by_date()
            elif search_selection == "b":
                search_by_time_spent()
            elif search_selection == "c":
                search_by_exact_title()
            elif search_selection == "d":
                search_by_regex()
            elif search_selection == "e":
                print(menu_options)
                break
            elif search_selection != "a" or search_selection != "b" or search_selection != "c" or search_selection != "d" or search_selection != "e":
                raise ValueError
        except ValueError:
            print("You must select a valid option. (a, b, c, d, or e)")


def search_by_date():
    pass


def search_by_time_spent():
    pass


def search_by_exact_title():
    pass


def search_by_regex():
    pass


if __name__ == "__main__":
    with open("work_log.csv", "w", newline="") as csvfile:
        fieldnames = ["Title", "Task Date", "Time", "Notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    main_menu()
