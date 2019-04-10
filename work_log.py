def main_menu():
    print("""
    Work Log

    Please select from the menu below what you would like to do?
    a) Add a new entry
    b) Search in existing entries
    c) Quit program
    """)

    while True:
        try:
            menu_selection = input("> ").lower()
            if menu_selection == "a":
                new_entry()
            elif menu_selection == "b":
                search_entries()
            elif menu_selection == "c":
                break
            elif menu_selection != "a" or menu_selection != "b" or menu_selection != "c":
                raise ValueError
        except ValueError:
            print("Must select a valid option.")


def new_entry():
    pass


def search_entries():
    pass


main_menu()
