
# colours
RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def vypis_menu():
    print("[1] Insert menu")
    print("[2] Update menu")
    print("[3] Remove menu")
    print("[4] List menu")
    print("[9] to terminate")


def vypis_insert_menu():
    print("[1] to insert a teacher")
    print("[2] to insert a course")
    print("[3] to insert a student")
    print("[9] to go back")


def vypis_update_menu():
    print("[1] to add a course to the teacher")
    print("[2] to add a course to the student")
    print("[3] to update student's grade")
    print("[9] to go back")


# odober studentovi kurz
# odober ucitelovi kurz
def vypis_remove_menu():
    print("[1] to remove teacher's course")
    print("[2] to remove student's course")
    print("[8] to remove tables")
    print("[9] to go back")


def vypis_list_menu():
    print("[1] to list teachers")
    print("[2] to list courses")
    print("[3] to list students")
    print("[9] to go back")