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


########################################################################################################################


def add_course_to_teacher(conn, cur):
    # ZISTIT CI NEJAKY COURSE JE BEZ UCITELA
    try:
        sql_command = sql.SQL(
            """
            SELECT *
            FROM courses
            WHERE teacher_id IS null
            """
        )
        cur.execute(sql_command)
        output_kurzy = cur.fetchall()
    except Exception as e:
        print(f"ERROR add_course_to_teacher(): {e}")
        conn.rollback()
    if len(output_kurzy) == 0:
        print("There is no course that have no teacher..")
        return
    print("Enter name of a teacher: ")
    name = input_only_letters()
    print("Enter surname of a teacher: ")
    surname = input_only_letters()

    # CHECK IF TEACHER EXISTS
    try:
        sql_command = sql.SQL(
            """
            SELECT *
            FROM teachers
            WHERE name = {} AND surname = {}
            """
        ).format(
            sql.Literal(name),
            sql.Literal(surname)
        )
        cur.execute(sql_command)
        output_teacher = cur.fetchall()
    except Exception as e:
        print(f"ERROR add_course_to_teacher(): {e}")
        conn.rollback()

    if len(output_teacher) == 0:
        print("There is no teacher with this name..")
        return

    # VYPIS KURZOV BEZ UCITELA
    print("Vyber si z nasledujúcich kurzov:")
    count = 1
    all_courses_id = []
    for kurz in output_kurzy:
        print(f"[{count}] {kurz['name']}")
        all_courses_id.append(kurz['course_id'])
        count += 1
    print("Vyber číslo kurzu: ", end='')
    cislo_kurzu = input_number_from_to(0, count)

    # ZISTIT AKE ID JE VYBRANE CISLO
    id_kurzu = all_courses_id[cislo_kurzu-1]
    for ucitel in output_teacher:
        id_ucitela = ucitel['teacher_id']

    # PRIRADIT KURZ UCITELOVI
    try:
        sql_command = sql.SQL(
            """
            UPDATE courses
            SET teacher_id = {}
            WHERE course_id = {}
            """
        ).format(
            sql.Literal(id_ucitela),
            sql.Literal(id_kurzu)
        )
        cur.execute(sql_command)
        conn.commit()
    except Exception as e:
        print(f"ERROR assigning course to teacher: {e}")
        conn.rollback()
    print(GREEN + "Successfully added course to the teacher!" + RESET)
    print("*****************************")

def add_course_to_student(conn, cur):
    # vyber ktoremu studentovi sa bude pridavat kurz
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM students
            """
        )
        cur.execute(sql_command)
        output_studenti = cur.fetchall()
    except Exception as e:
        print(f"ERROR assigning course to student: {e}")
        conn.rollback()

    count_st = 0
    all_students_id = []
    for student in output_studenti:
        print(f"[{count_st}] {student['name']} {student['surname']} ({student['grade']})")
        all_students_id.append(student['student_id'])
        count_st += 1
    print("Vyber studenta: ")
    cislo_studenta = input_number_from_to(0, count_st-1)

    # ziskanie ID studenta
    id_studenta = all_students_id[cislo_studenta]

    # vyber z dostupnych kurzov
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM courses
            """
        )
        cur.execute(sql_command)
        output_courses = cur.fetchall()
    except Exception as e:
        print(f"ERROR SELECT * FROM courses: {e}")
        conn.rollback()

    #ziskanie ID dostupnych kurzov
    all_courses_id = []
    for course in output_courses:
        all_courses_id.append(course['course_id'])

    # ziskanie vybranych kurzov
    all_chosed_numbers_co = []
    while True:
        count_co = 0
        print(f"Actual courses: {all_chosed_numbers_co}")
        for course in output_courses:
            print(f"[{count_co}] {course['name']}")
            count_co += 1
        while True:
            print("Vyber kurzu: ")
            cislo_kurzu = input_number_from_to(-1, count_co - 1)
            if cislo_kurzu not in all_chosed_numbers_co:
                break
            else:
                print("This course have already been chosen!")
        if cislo_kurzu == -1:
            break
        all_chosed_numbers_co.append(cislo_kurzu)

    # ziskanie ID vsetkych vybranych kurzov
    final_courses_id = []
    for course_number in all_chosed_numbers_co:
        final_courses_id.append(all_courses_id[course_number])

    # pridanie do spojovacej tabulky
    for kurz in final_courses_id:
        try:
            sql_command = sql.SQL(
                """
                INSERT INTO courses_students ("Course_Id","Student_Id") VALUES({},{})
                """
            ).format(
                sql.Literal(kurz),
                sql.Literal(id_studenta)
            )
            cur.execute(sql_command)
            conn.commit()
        except Exception as e:
            print(f"ERROR SELECT * FROM courses: {e}")
            conn.rollback()
    print(GREEN + "Successfully added course to the student!" + RESET)
    print("*****************************")


















def update_students_grade(conn, cur):
    print("update_students_grade")


