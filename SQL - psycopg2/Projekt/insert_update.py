from funkcie import *
from vypisy import *

def insert_student(conn, cur):
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

    print(GREEN + "Successfully inserted a student!" + RESET)
    print("*****************************")


def insert_course(conn, cur):
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
    print(GREEN + "Successfully inserted a course!" + RESET)
    print("*****************************")




def insert_teacher(conn, cur):
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
        print(GREEN + "Successfully inserted a teacher!" + RESET)
        print("*****************************")

    except Exception as e:
        print(f"Issue while inserting a teacher..: {e}")
        conn.rollback()











def add_course_to_teacher(conn, cur):
    print("add_course_to_teacher")


def update_students_courses(conn, cur):
    print("update_students_courses")

def update_students_grade(conn, cur):
    print("update_students_grade")

