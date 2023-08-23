import psycopg2.extras
from psycopg2 import sql
import sys


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
    print("[2] to update student's courses")
    print("[3] to update student's grade")
    print("[9] to go back")


def vypis_remove_menu():
    print("[8] to drop tables")
    print("[9] to go back")


def vypis_list_menu():
    print("[1] to list teachers")
    print("[2] to list courses")
    print("[3] to list students")
    print("[9] to go back")

def add_course_to_teacher():
    print("add_course_to_teacher")


def update_students_courses():
    print("update_students_courses")

def update_students_grade():
    print("update_students_grade")


def list_table(conn, cur, table):
    print(f"List of {table}: ")
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM {};
            """
        ).format(
            sql.Identifier(table)
        )
        cur.execute(sql_command)
        output = cur.fetchall()
        for nieco in output:
            print(nieco[1])
        #print(output)
    except Exception as e:
        print(f"Chyba pri listovaní tabuľky: {e}")
        conn.rollback()

def vytvor_tabulky(conn, cur, tables, ids):
    try:
        sql_command = sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {} 
            (
                {} SERIAL PRIMARY KEY,
                name VARCHAR(20),
                surname VARCHAR(20),
                grade INT
            );
            CREATE TABLE IF NOT EXISTS {} 
            (
                {} SERIAL PRIMARY KEY,
                name VARCHAR(20),
                surname VARCHAR(20),
                degree VARCHAR(10)
            );
            CREATE TABLE IF NOT EXISTS {} 
            (
                {} SERIAL PRIMARY KEY,
                name VARCHAR(20),
                teacher_id INT
            );
            CREATE TABLE IF NOT EXISTS courses_students
            (
                "Course_Id" INT,
                "Student_Id" INT,
                CONSTRAINT "PK_Courses_Students" PRIMARY KEY ("Course_Id","Student_Id")
            );
            """
        ).format(
            sql.Identifier(tables[0]),
            sql.Identifier(ids[0]),
            sql.Identifier(tables[1]),
            sql.Identifier(ids[1]),
            sql.Identifier(tables[2]),
            sql.Identifier(ids[2])
        )
        cur.execute(sql_command)
        conn.commit()
    except Exception as e:
        print(f"Issue with creating table: {e}")
        conn.rollback()
        cur.close()
        sys.exit(1)

def input_only_letters():
    while True:
        try:
            user_input = input()
            if user_input.isalpha():
                break
            else:
                print("Invalid input. Please enter only letters.")
                continue
        except Exception as e:
            print("Issue while retrieving a string: ")
    return user_input


def vstupy_ucitela():
    #name, surname, degree
    vysl = []
    print("Enter teachers name: ",end='')
    vysl.append(input_only_letters())
    print("Enter teachers surname: ", end='')
    vysl.append(input_only_letters())
    print("Enter teachers degree: ", end='')
    vysl.append(input_only_letters())
    return vysl


def insert_teacher():
    print(f"Inserting a teacher..")
    vstupy = vstupy_ucitela()
    vstupy[2] = vstupy[2] + '.'
    try:
        sql_command = sql.SQL(
            """
            INSERT INTO teachers(name, surname, degree) VALUES ({}, {}, {});
            """
        ).format(
            sql.Literal(vstupy[0]),
            sql.Literal(vstupy[1]),
            sql.Literal(vstupy[2])
        )
        cur.execute(sql_command)
        conn.commit()
        print("Successfully inserted a teacher!")
        print("*****************************")

    except Exception as e:
        print(f"Issue while inserting a teacher..: {e}")
        conn.rollback()


def insert_course():
    print(f"Inserting a course..")
    print("Zadaj názov kurzu: ", end='')
    name = input_only_letters()
    print("Vyber si, ktorý učiteľ má učiť tento predmet: ")
    try:
        sql_command = sql.SQL(
            """
            SELECT name, surname, teacher_id
            FROM teachers
            """
        )
        cur.execute(sql_command)
    except Exception as e:
        print(f"Error inserting a course: {e}")
    output = cur.fetchall()
    count = 0
    for ucitel in output:
        print(f"{ucitel['name']} {ucitel['surname']} ({count})")
        count += 1
    print("Choice: ", end='')
    while True:
        try:
            input_ucitel = int(input())
            if 0 <= input_ucitel < count:
                break
            else:
                print("Musíš zadať správne číslo!")
        except ValueError:
            print("Musíš zadať číslo!")
        except Exception as e:
            print(f"Error during input: {e}")

    # treba zistit meno ucitela, ktoremu bolo priradene cislo
    count2 = 0
    for ucitel in output:
        if input_ucitel == count2:
            meno_ucitela = ucitel['name']
            break
        count2 += 1

    ucitel_id = -1
    # treba zistit ID ucitela
    for riadok in output:
        if riadok['name'] == meno_ucitela:
            ucitel_id = riadok['teacher_id']

    try:
        sql_command = sql.SQL(
            """INSERT INTO courses (name, teacher_id)
                VALUES({},{})"""
        ).format(
            sql.Literal(name),
            sql.Literal(ucitel_id)
        )
        cur.execute(sql_command)
        conn.commit()
    except Exception as e:
        print(f"Error adding a course to the table courses: {e}")
        conn.rollback()
    print("Successfully inserted a course!")
    print("*****************************")


def list_students(conn, cur, table):
    print(f"List of {table}: ")
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM {};
            """
        ).format(
            sql.Identifier(table)
        )
        cur.execute(sql_command)
        output = cur.fetchall()
        for student in output:
            print(f"    {student['name']} {student['surname']} ({student['grade']})")
        print("*****************************")

    except Exception as e:
        print(f"Chyba pri listovaní tabuľky: {e}")
        conn.rollback()


def list_teachers(conn, cur, table):
    print(f"List of {table}: ")
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM {};
            """
        ).format(
            sql.Identifier(table)
        )
        cur.execute(sql_command)
        output = cur.fetchall()
        for teacher in output:
            print(f"    {teacher['degree']} {teacher['name']} {teacher['surname']}")
        print("*****************************")

    except Exception as e:
        print(f"Chyba pri listovaní tabuľky: {e}")
        conn.rollback()


def join_tables_curses_teachers():
    try:
        sql_command = sql.SQL(
            """
            SELECT co.name as nazov_kurzu, te.name as meno_ucitela, te.surname as priezvisko_ucitela, *
            FROM courses as co
            JOIN teachers as te
            	ON co.teacher_id = te.teacher_id
            """
        )
        cur.execute(sql_command)
        return cur.fetchall()
    except Exception as e:
        print(f"Nastala chyba pri joinovaní tabuliek courses, teachers: {e}")
        conn.rollback()


def vytvor_spojovaciu_tabulku(conn, cur):
    try:
        sql_command = sql.SQL(
            """
            SELECT co.name as nazov_kurzu, st.name as meno_ziaka, *
            FROM courses_students as cs
            JOIN courses as co
            	ON cs."Course_Id" = co.course_id
            JOIN students as st
            	ON cs."Student_Id" = st.student_id
            """
        )
        cur.execute(sql_command)
        return cur.fetchall()
    except Exception as e:
        print(f"Nastala chyba pri vytvárani spojovacej tabulky: {e}")
        conn.rollback()

def list_courses(conn, cur, table):
    print(f"List of {table}: ")
    try:
        joined_tables = join_tables_curses_teachers()

        students_list = []
        for row in joined_tables:
            print(f"Subject: {row['nazov_kurzu']}")
            print(f"    Teacher: {row['meno_ucitela']} {row['priezvisko_ucitela']}")
            spojovacia_tabulka = vytvor_spojovaciu_tabulku(conn,cur)
            for row_ST in spojovacia_tabulka:
                if row_ST['nazov_kurzu'] == row['nazov_kurzu']:
                    students_list.append(f"{row_ST['meno_ziaka']} {row_ST['surname']}")

            students_string = ", ".join(students_list)
            print(f"    Students: {students_string}")
            students_list = []
        print("*****************************")

    except Exception as e:
        print(f"Chyba pri listovaní tabuľky kurov: {e}")
        conn.rollback()


def drop_tables(tables):
    try:
        sql_command = sql.SQL(
            """
            DROP TABLE IF EXISTS {};
            DROP TABLE IF EXISTS {};
            DROP TABLE IF EXISTS {};
            DROP TABLE IF EXISTS courses_students
            """
        ).format(
            sql.Identifier(tables[0]),
            sql.Identifier(tables[1]),
            sql.Identifier(tables[2])
        )
        cur.execute(sql_command)
        conn.commit()
    except Exception as e:
        print(f"Chyba pri mazaní tabuľky: {e}")
        conn.rollback()
        cur.close()
        sys.exit(1)

    print("Successfully dropped all tables!")
    print("*****************************")

def vstupy_ziaka():
    #name, surname, grade
    vysl = []
    print("Enter students name: ",end='')
    vysl.append(input_only_letters())
    print("Enter students surname: ", end='')
    vysl.append(input_only_letters())
    while True:
        print("Enter students grade: ", end='')
        try:
            pom = int(input())
            if pom >= 1:
                break
            else:
                print("Musíš zadať správne číslo!")
                continue
        except Exception as e:
            print(f"Issue with int input: {e}")
    vysl.append(pom)
    return vysl


def insert_student():
    # vypytat meno, priezvisko, rocnik
    input_student = vstupy_ziaka()
    # pridat ho do studentskej databazy
    try:
        sql_command = sql.SQL(
            """
            INSERT INTO students(name, surname, grade) VALUES ({}, {}, {});
            """
        ).format(
            sql.Literal(input_student[0]),
            sql.Literal(input_student[1]),
            sql.Literal(input_student[2])
        )
        cur.execute(sql_command)
        conn.commit()

    except Exception as e:
        print(f"Issue while inserting a student..: {e}")
        conn.rollback()

    # vyber z kurzov
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM courses;
            """
        )
        cur.execute(sql_command)
        output_courses = cur.fetchall()
    except Exception as e:
        print(f"Issue while inserting a student..: {e}")
        conn.rollback()

    all_courses = []
    all_courses_id = []
    count_added_courses = 0
    while True:
        mena_kurzov = []
        print(f"Aktuálne kurzy: {all_courses}")
        count = 0
        for kurz in output_courses:
            print(f"{count}, {kurz['name']}")
            mena_kurzov.append(kurz['name'])
            count += 1
        while True: # osetrenie zadania cisla
            print("Vyber si z nasledujúcich kurzov: (-1 pre ukončenie): ", end='')
            try:
                number = int(input())
                if (-1 <= number < count):
                    break
                else:
                    print("Musíš zadať správne číslo!")
                    continue
            except Exception as e:
                print(f"Issue with int input: {e}")
                conn.rollback()
        if number == -1:
            break

        all_courses.append(number)

        # zistenie ID kurzov
        for kurz in output_courses:
            if kurz['name'] == mena_kurzov[number]:
                all_courses_id.append(kurz['course_id'])

        count_added_courses += 1
        if count_added_courses == count:
            break

    # zistenie ID studenta
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM students;
            """
        )
        cur.execute(sql_command)
        output_students = cur.fetchall()
    except Exception as e:
        print(f"Issue while inserting a student..: {e}")
        conn.rollback()

    for student in output_students:
        if student['name'] == input_student[0] and student['surname'] == input_student[1]:
            actual_student_id = student['student_id']

    # pridat do spojovacej tabulky
    for kurz_id in all_courses_id:
        try:
            sql_command = sql.SQL(
                """
                INSERT INTO courses_students("Course_Id", "Student_Id") VALUES({}, {});
                """
            ).format(
                sql.Literal(kurz_id),
                sql.Literal(actual_student_id),
            )
            cur.execute(sql_command)
            conn.commit()

        except Exception as e:
            print(f"Issue while inserting a student..: {e}")
            conn.rollback()

    print("Successfully inserted a student!")
    print("*****************************")

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
            print("Chyba pri konektovaní na databázu: ")


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

                # odober studentovi kurz
                # odober ucitelovi kurz

                # osetrit vstupy pre menu2

            if menu_choice == 1:  # DONE
                # INSERT
                while True:
                    print("INSERT MENU!")
                    vypis_insert_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 1:
                        insert_teacher()  # INSERT A TEACHER
                    if menu_choice2 == 2:
                        insert_course()  # INSERT A COURSE
                    if menu_choice2 == 3:
                        insert_student()  # INSERT A STUDENT
                    if menu_choice2 == 9:
                        break

            if menu_choice == 2:
                # UPDATE
                while True:
                    print("UPDATE MENU!")
                    vypis_update_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 1:
                        add_course_to_teacher()  # COURSE TO TEACHER
                    if menu_choice2 == 2:
                        update_students_courses()  # STUDENTS COURSES
                    if menu_choice2 == 3:
                        update_students_grade()  # STUDENTS GRADE
                    if menu_choice2 == 9:
                        break

            if menu_choice == 3:
                # REMOVE
                while True:
                    print("REMOVE MENU!")
                    vypis_remove_menu()
                    menu_choice2 = int(input("Menu choice: "))
                    if menu_choice2 == 8:
                        drop_tables(tables)  # DROP TABLES
                    if menu_choice2 == 9:
                        break

            if menu_choice == 4: # DONE
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
