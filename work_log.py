import datetime
import csv
import re


def main_menu():
    menu_options = """
    Work Log Main Menu
    Please select from the options below?
    a) Add a new entry
    b) Search in existing entries
    c) Quit program
    """

    while True:
        try:
            print(menu_options)
            menu_selection = input("> ").lower()
            if menu_selection == "a":
                new_entry()
            elif menu_selection == "b":
                search_menu()
            elif menu_selection == "c":
                break
            elif menu_selection != "a" or menu_selection != "b" or menu_selection != "c":
                raise ValueError
        except ValueError:
            print("You must select a valid option. (a, b, or c)")


def new_entry():
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


def search_menu():
    list_by_title = []
    list_by_date = []
    list_by_time = []
    list_by_notes = []
    with open("work_log.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        for word in rows:
            list_by_title.append(word["Title"])
            list_by_date.append(datetime.datetime.strptime(word["Task Date"], "%d-%m-%Y"))
            list_by_time.append(int(word["Time"]))
            list_by_notes.append(word["Notes"])

    search_menu = """
    Search Menu
    Please select from the options below?
    a) Search by range of dates
    b) Search by specific date
    c) Search by time spent
    d) Search by word
    e) Search by regex
    f) Previous menu
    """

    while True:
        try:
            print(search_menu)
            search_selection = input("> ").lower()
            if search_selection == "a":
                search_range_of_dates(list_by_title, list_by_date, list_by_time, list_by_notes)
            elif search_selection == "b":
                search_specific_date(list_by_title, list_by_date, list_by_time, list_by_notes)
            elif search_selection == "c":
                search_by_time_spent(list_by_title, list_by_date, list_by_time, list_by_notes)
            elif search_selection == "d":
                search_by_word(list_by_title, list_by_date, list_by_time, list_by_notes)
            elif search_selection == "e":
                search_by_regex(list_by_title, list_by_date, list_by_time, list_by_notes)
            elif search_selection == "f":
                break
            elif search_selection != "a" or search_selection != "b" or search_selection != "c" or search_selection != "d" or search_selection != "e":
                raise ValueError
        except ValueError:
            print("You must select a valid option. (a, b, c, d, or e)")


def search_specific_date(list_by_title, list_by_date, list_by_time, list_by_notes):
    timestamp_list = []
    for date in list_by_date:
        timestamp_list.append(round(datetime.datetime.timestamp(date)))
    while True:
        try:
            search_date = input("Please enter your date (DD-MM-YYYY): ")
            strp_search_date = datetime.datetime.strptime(search_date, "%d-%m-%Y")
        except ValueError:
            print("You must use the following date format DD-MM-YYYY")
        else:
            timestamp_search_date = round(datetime.datetime.timestamp(strp_search_date))
            break
    index_positions_date = [i for (i, date) in enumerate(
        timestamp_list) if date == timestamp_search_date]
    if len(index_positions_date) == 0:
        print("Unfortunately there are no entries that match {}".format(search_date))
    else:
        for match in index_positions_date:
            print("""
                    Title: {}
                    Date: {}
                    Time spent in minutes: {}
                    Optional notes: {}
                    """.format(
                list_by_title[match],
                list_by_date[match].strftime("%B %d %Y"),
                list_by_time[match],
                list_by_notes[match]))


def search_range_of_dates(list_by_title, list_by_date, list_by_time, list_by_notes):
    timestamp_list = []
    for date in list_by_date:
        timestamp_list.append(round(datetime.datetime.timestamp(date)))
    while True:
        try:
            start_date = input("Please enter start date (DD-MM-YYYY): ")
            strp_start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
        except ValueError:
            print("You must use the following date format DD-MM-YYYY")
        else:
            timestamp_start_date = round(datetime.datetime.timestamp(strp_start_date))
            while True:
                try:
                    end_date = input("Please enter end date (DD-MM-YYYY): ")
                    strp_end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y")
                except ValueError:
                    print("You must use the following date format DD-MM-YYYY")
                else:
                    timestamp_end_date = round(datetime.datetime.timestamp(strp_end_date))
                    break
            break
    index_positions_date = [i for (i, date) in enumerate(
        timestamp_list) if date in range(timestamp_start_date, timestamp_end_date + 1)]
    if len(index_positions_date) == 0:
        print("Unfortunately there are no entries that match {} to {}".format(start_date, end_date))
    else:
        for match in index_positions_date:
            print("""
                    Title: {}
                    Date: {}
                    Time spent in minutes: {}
                    Optional notes: {}
                    """.format(
                list_by_title[match],
                list_by_date[match].strftime("%B %d %Y"),
                list_by_time[match],
                list_by_notes[match]))


def search_by_time_spent(list_by_title, list_by_date, list_by_time, list_by_notes):
    try:
        search_time = int(input("How many minutes would you like to search by: "))
    except ValueError:
        print("You must use rounded minutes. example: 120")
    else:
        index_positions_time = [i for (i, time) in enumerate(list_by_time) if time == search_time]
        if len(index_positions_time) == 0:
            print("We are sorry but we did not find an exact match in time")
        else:
            for match in index_positions_time:
                print("""
                Title: {}
                Date: {}
                Time spent in minutes: {}
                Optional notes: {}
                """.format(
                    list_by_title[match],
                    list_by_date[match].strftime("%B %d %Y"),
                    list_by_time[match],
                    list_by_notes[match]))


def search_by_word(list_by_title, list_by_date, list_by_time, list_by_notes):
    search_word = input("Which word are you looking for: ")
    index_positions_notes = [i for (i, note) in enumerate(list_by_notes) if search_word in note]
    index_positions_titles = [i for (i, title) in enumerate(list_by_title) if title == search_word]
    index_positions_combined = list(set(index_positions_notes + index_positions_titles))

    if len(index_positions_combined) == 0:
        print("We are sorry but we did not find a match for {}".format(search_word))
    else:
        for match in index_positions_combined:
            print("""
            Title: {}
            Date: {}
            Time spent in minutes: {}
            Optional notes: {}
            """.format(
                list_by_title[match],
                list_by_date[match].strftime("%B %d %Y"),
                list_by_time[match],
                list_by_notes[match]))


def search_by_regex(list_by_title, list_by_date, list_by_time, list_by_notes):
    with open("work_log.csv", "r", newline="") as csvfile:
        data = csvfile.read()

    pattern_search = input(r"What type of pattern are you looking for: ")

    my_list = re.findall(pattern_search, data, re.X)
    title_index_list = [i for (i, word) in enumerate(list_by_title) if word in my_list]
    notes_index_list = [i for (i, word) in enumerate(list_by_notes) if word in my_list]
    index_positions_combined = list(set(title_index_list + notes_index_list))

    if len(index_positions_combined) == 0:
        print("We are sorry but we did not find a match for {}".format(pattern_search))
    else:
        for match in index_positions_combined:
            print("""
            Title: {}
            Date: {}
            Time spent in minutes: {}
            Optional notes: {}
            """.format(
                list_by_title[match],
                list_by_date[match].strftime("%B %d %Y"),
                list_by_time[match],
                list_by_notes[match]))


if __name__ == "__main__":
    # with open("work_log.csv", "w", newline="") as csvfile:
    #     fieldnames = ["Title", "Task Date", "Time", "Notes"]
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #
    #     writer.writeheader()
    main_menu()
