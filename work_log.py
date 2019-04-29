import csv
import datetime
import re


def create_work_log():
    # This function is the logic for the work_log
    list_by_title = []
    list_by_date = []
    list_by_time = []
    list_by_notes = []
    timestamp_list = []

    while True:
        menu_selection = main_menu()
        if menu_selection == "a":
            new_entry()
            print("Your entry has been recorded.")
        elif menu_selection == "b":
            # The code below clears all the list to not have duplicates when appending
            list_by_title.clear()
            list_by_date.clear()
            list_by_time.clear()
            list_by_notes.clear()
            timestamp_list.clear()
            # Code below for appending data from csv into the lists above
            with open("work_log.csv", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                for word in rows:
                    list_by_title.append(word["Title"])
                    list_by_date.append(datetime.datetime.strptime(
                                        word["Task Date"], "%d-%m-%Y"))
                    list_by_time.append(int(word["Time"]))
                    list_by_notes.append(word["Notes"])
            # Code below is for appending and converting my list of dates to timestamps
            for date in list_by_date:
                timestamp_list.append(round(datetime.datetime.timestamp(date)))

            while True:
                if len(list_by_title) == 0:
                    print("We are sorry but there are no entries to search.")
                    break
                else:
                    search_selection = search_menu()

                    if search_selection == "a":
                        index_list = search_range_of_dates(list_by_title,
                                                           list_by_date,
                                                           list_by_time,
                                                           list_by_notes,
                                                           timestamp_list)
                        if index_list:
                            show_results(list_by_title, list_by_date,
                                         list_by_time, list_by_notes,
                                         index_list)
                    elif search_selection == "b":
                        index_list = search_specific_date(list_by_title,
                                                          list_by_date,
                                                          list_by_time,
                                                          list_by_notes,
                                                          timestamp_list)
                        if index_list:
                            show_results(list_by_title, list_by_date,
                                         list_by_time, list_by_notes,
                                         index_list)
                    elif search_selection == "c":
                        index_list = search_by_time_spent(list_by_title,
                                                          list_by_date,
                                                          list_by_time,
                                                          list_by_notes)
                        if index_list:
                            show_results(list_by_title, list_by_date,
                                         list_by_time, list_by_notes,
                                         index_list)
                    elif search_selection == "d":
                        index_list = search_by_word(list_by_title, list_by_date,
                                                    list_by_time, list_by_notes)
                        if index_list:
                            show_results(list_by_title, list_by_date,
                                         list_by_time, list_by_notes,
                                         index_list)
                    elif search_selection == "e":
                        index_list = search_by_regex(list_by_title, list_by_date,
                                                     list_by_time, list_by_notes)
                        if index_list:
                            show_results(list_by_title, list_by_date,
                                         list_by_time, list_by_notes,
                                         index_list)
                    elif search_selection == "f":
                        break
        elif menu_selection == "c":
            break


def main_menu():
    # This function shows the main menu and returns the input from user
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
            if (menu_selection == "a"
                    or menu_selection == "b"
                    or menu_selection == "c"):
                return menu_selection
            elif (menu_selection != "a"
                    or menu_selection != "b"
                    or menu_selection != "c"):
                raise ValueError
        except ValueError:
            print("You must select a valid option. (a, b, or c)")


def new_entry():
    # This function takes the information from the user and writes to the csv
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
                    time_spent = int(input(
                        "Time spent on task. (Rounded Minutes): "))
                except ValueError:
                    print("You must use rounded minutes. example: 12 ")
                else:
                    break
            break
    optional_notes = input("Optional notes. (You may leave this blank): ")

    write_to_csv_file(title, fmt_task_date, time_spent, optional_notes)


def write_to_csv_file(title, fmt_task_date, time_spent, optional_notes):
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
    # This function shows the search menu and return the input from user
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
            if (search_selection == "a"
                    or search_selection == "b"
                    or search_selection == "c"
                    or search_selection == "d"
                    or search_selection == "e"
                    or search_selection == "f"):
                return search_selection
            elif (search_selection != "a"
                    or search_selection != "b"
                    or search_selection != "c"
                    or search_selection != "d"
                    or search_selection != "e"
                    or search_selection != "f"):
                raise ValueError
        except ValueError:
            print("You must select a valid option. (a, b, c, d, e, f)")


def search_range_of_dates(list_by_title, list_by_date, list_by_time,
                          list_by_notes, timestamp_list):
    # This function searches from a range of dates and returns the index positions
    while True:
        try:
            start_date = input("Please enter start date (DD-MM-YYYY): ")
            strp_start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
        except ValueError:
            print("You must use the following date format DD-MM-YYYY")
        else:
            timestamp_start_date = round(
                datetime.datetime.timestamp(strp_start_date))
            while True:
                try:
                    end_date = input("Please enter end date (DD-MM-YYYY): ")
                    strp_end_date = datetime.datetime.strptime(end_date,
                                                               "%d-%m-%Y")
                except ValueError:
                    print("You must use the following date format DD-MM-YYYY")
                else:
                    timestamp_end_date = round(
                        datetime.datetime.timestamp(strp_end_date))
                    break
            break
    # Code below creates a list of index matching the date ranges given to the timestamp_list
    index_positions_date = [i for (i, date) in enumerate(timestamp_list)
                            if date in range(timestamp_start_date,
                                             timestamp_end_date + 1)]

    if len(index_positions_date) == 0:
        print("There are no entries that match {} to {}".format(start_date,
                                                                end_date))
    else:
        return index_positions_date


def search_specific_date(list_by_title, list_by_date, list_by_time,
                         list_by_notes, timestamp_list):
    # This function searches from a specific date and returns the index positions
    strf_list_of_dates = []

    for date in list_by_date:
        strf_list_of_dates.append(date.strftime("%d-%m-%Y"))

    while True:
        try:
            print("Here is a list of dates available {} ".format(strf_list_of_dates))
            search_date = input("Please enter your date (DD-MM-YYYY): ")
            strp_search_date = datetime.datetime.strptime(
                search_date, "%d-%m-%Y")
        except ValueError:
            print("You must use the following date format DD-MM-YYYY")
        else:
            timestamp_search_date = round(datetime.datetime.timestamp(
                strp_search_date))
            break
    # Code below creates a list of index matching the specific date given to the timestamp_list
    index_positions_date = [i for (i, date) in enumerate(timestamp_list)
                            if date == timestamp_search_date]

    if len(index_positions_date) == 0:
        print("Unfortunately there are no entries that match {}".format(
            search_date))
    else:
        return index_positions_date


def search_by_time_spent(list_by_title, list_by_date, list_by_time,
                         list_by_notes):
    # This function returns the index positions of a user input search time from list_by_time
    try:
        search_time = int(input(
            "How many minutes would you like to search by: "))
    except ValueError:
        print("You must use rounded minutes. example: 120")
    else:
        index_positions_time = [i for (i, time) in enumerate(list_by_time)
                                if time == search_time]
        if len(index_positions_time) == 0:
            print("We are sorry but we did not find an exact match in time")
        else:
            return index_positions_time


def search_by_word(list_by_title, list_by_date, list_by_time, list_by_notes):
    # This function returns the index positions from a user input word from list_by_title and list_by_notes
    search_word = input("Which word are you looking for: ")

    index_positions_notes = [i for (i, note) in enumerate(list_by_notes)
                             if search_word in note]
    index_positions_titles = [i for (i, title) in enumerate(list_by_title)
                              if title == search_word]
    index_positions_combined = list(set(index_positions_notes
                                        + index_positions_titles))

    if len(index_positions_combined) == 0:
        print("We are sorry but we did not find a match for {}".format(
            search_word))
    else:
        return index_positions_combined


def search_by_regex(list_by_title, list_by_date, list_by_time, list_by_notes):
    # This function returns the index position from the list using user input searching by patterns
    with open("work_log.csv", "r", newline="") as csvfile:
        data = csvfile.read()

    try:
        pattern_search = re.compile(input(r"What type of pattern are you looking for: "), re.X)
    except re.error:
        print("Unfortunately that is not a valid regex.")
    else:
        my_list = pattern_search.findall(data)
        title_index_list = [i for (i, word) in enumerate(list_by_title)
                            if word in my_list]
        notes_index_list = [i for (i, word) in enumerate(list_by_notes)
                            if word in my_list]
        index_positions_combined = list(set(title_index_list + notes_index_list))

        if len(index_positions_combined) == 0:
            print("We are sorry but we did not find a match for {}".format(
                pattern_search))
            print("You can try using a similar format to [\w]+ ")
        else:
            return index_positions_combined


def show_results(list_by_title, list_by_date, list_by_time, list_by_notes,
                 index_list):
    # This function prints the results to the console.
    for match in index_list:
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
    create_work_log()
