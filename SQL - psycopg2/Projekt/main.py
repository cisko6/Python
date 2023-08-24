import psycopg2.extras

from insert_update import *
from remove_list import *

if __name__ == "__main__":
    while True:
        try:
            #vysl = input("Zadaj heslo do databazy: ")
            vysl = "cisco"

            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                port=5432,
                user="postgres",
                password=vysl
            )
            break
        except Exception as e:
            print(f"Chyba pri konektovaní na databázu: {e}")


    # Identifikátory
    tables = ["students", "teachers", "courses"]
    ids = ["student_id", "teacher_id", "course_id"]

    with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        vytvor_tabulky(conn, cur, tables, ids)
        while True:
            while True:
                print("Welcome at school!")
                vypis_menu()
                try:
                    menu_choice = int(input("Menu choice: "))
                    if 0 <= menu_choice <= 6 or 8 <= menu_choice <= 9:
                        break
                except ValueError as e:
                    print(f"Zadaj cislo! Chyba: {e}")

                # osetrit vstupy pre menu2
                # pri listovani studentov uviest kolko ich je

            if menu_choice == 1:
                # INSERT
                while True:
                    print("INSERT MENU!")
                    vypis_insert_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 1:
                        insert_teacher(conn, cur)  # INSERT A TEACHER
                    if menu_choice2 == 2:
                        insert_course(conn, cur)  # INSERT A COURSE
                    if menu_choice2 == 3:
                        insert_student(conn, cur)  # INSERT A STUDENT
                    if menu_choice2 == 9:
                        break

            if menu_choice == 2:
                # UPDATE
                while True:
                    print("UPDATE MENU!")
                    vypis_update_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 1:
                        add_course_to_teacher(conn, cur)  # COURSE TO TEACHER
                    if menu_choice2 == 2:
                        add_course_to_student(conn, cur)  # COURSE TO STUDENT
                    if menu_choice2 == 3:
                        update_students_grade(conn, cur)  # STUDENTS GRADE
                    if menu_choice2 == 9:
                        break

            if menu_choice == 3:
                # REMOVE
                while True:
                    print("REMOVE MENU!")
                    vypis_remove_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 1:
                        remove_teachers_course(conn, cur)  # remove teacher's course
                    if menu_choice2 == 2:
                        remove_students_course(conn, cur)  # remove student's course
                    if menu_choice2 == 8:
                        drop_tables(conn, cur, tables)  # DROP TABLES
                    if menu_choice2 == 9:
                        break

            if menu_choice == 4:
                # LIST
                while True:
                    print("LIST MENU!")
                    vypis_list_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 1:
                        list_teachers(conn, cur, tables[1])  # LIST TEACHERS
                    if menu_choice2 == 2:
                        list_courses(conn, cur, tables[2])  # LIST COURSES
                    if menu_choice2 == 3:
                        list_students(conn, cur, tables[0])  # LIST STUDENTS
                    if menu_choice2 == 9:
                        break

            if menu_choice == 9:
                print("BYE!")
                break

    cur.close()
    conn.close()
    print(conn.closed)
