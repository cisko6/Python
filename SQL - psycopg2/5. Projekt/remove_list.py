from funkcie import *
from vypisy import *

def drop_tables(conn, cur, tables):
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

    print(GREEN + "Successfully dropped all tables!" + RESET)
    print("*****************************")


def remove_students_course(conn, cur):
    # ZISTIT STUDENTA
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM students
            """
        )
        cur.execute(sql_command)
        output_students = cur.fetchall()
    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()

    # vypis vsetkych ucitelov a ziskanie ich id
    count_st = 0
    all_students_id = []
    for student in output_students:
        print(f"[{count_st}] {student['name']} {student['surname']} ({student['grade']})")
        all_students_id.append(student['student_id'])
        count_st += 1

    print("Choose your student: ")
    chosed_student_number = input_number_from_to(0, count_st-1)

    # ZISTIT STUDENTOVE ID
    id_student = all_students_id[chosed_student_number]

    # ZISTIT ARRAY KURZOV KTORYCH SA UZ NECHCE ZUCASTNOVAT
    try:
        sql_command = sql.SQL(
            """
            SELECT *
            FROM courses as co
            JOIN courses_students as cs
                ON co.course_id = cs."Course_Id"
            WHERE "Student_Id" = {}
            """
        ).format(
            sql.Literal(id_student)
        )
        cur.execute(sql_command)
        output_courses = cur.fetchall()
    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()

    if not output_courses:
        print("Tento študent nemá priradený žiadny kurz!")
        return

    chosed_courses = []
    while True:
        count_co = 0
        all_courses_id = []
        print(f"Already chosen courses {chosed_courses}")
        for course in output_courses:
            print(f"[{count_co}] {course['name']}")
            all_courses_id.append(course['course_id'])
            count_co += 1
        while True:
            print("Choose a course to be removed: (-1 to stop adding)")
            vysl = input_number_from_to(-1, count_co-1)
            if vysl not in chosed_courses:
                break
            else:
                print("You already chose this course!")
        if vysl == -1:
            break
        chosed_courses.append(vysl)

    #  ZISTIT ID PREMETOV
    final_courses_id = []
    for kurz in chosed_courses:
        final_courses_id.append(all_courses_id[kurz])

    # VYMAZAT ZO SPOJOVACEJ TABULKY
    for course in final_courses_id:
        try:
            sql_command = sql.SQL(
                """
                DELETE FROM courses_students
                WHERE "Course_Id" = {} AND "Student_Id" = {}
                """
            ).format(
                sql.Literal(course),
                sql.Literal(id_student)
            )
            cur.execute(sql_command)
            conn.commit()
        except Exception as e:
            print(f"ERROR removing teachers course: {e}")
            conn.rollback()

    print(GREEN + "Successfully removed students course!" + RESET)
    print("*****************************")


def remove_teachers_course(conn, cur):
    try:
        sql_command = sql.SQL(
            """
            SELECT * FROM teachers
            """
        )
        cur.execute(sql_command)
        output_teachers = cur.fetchall()
    except Exception as e:
        print(f"ERROR changing students grade: {e}")
        conn.rollback()

    # vypis vsetkych ucitelov a ziskanie ich id
    count_te = 0
    all_teachers_id = []
    for teacher in output_teachers:
        print(f"[{count_te}] {teacher['degree']} {teacher['surname']} {teacher['name']}")
        all_teachers_id.append(teacher['teacher_id'])
        count_te += 1

    print("Zvoľ učiteľa: ")
    chosed_teacher_number = input_number_from_to(0, count_te-1)

    # ziskanie ID učiteľa
    id_teacher = all_teachers_id[chosed_teacher_number]

    # ziskanie ucitelovych kurzov
    try:
        sql_command = sql.SQL(
            """
            SELECT *
            FROM courses
            WHERE teacher_id = {}
            """
        ).format(
            sql.Literal(id_teacher)
        )
        cur.execute(sql_command)
        output_courses = cur.fetchall()
    except Exception as e:
        print(f"ERROR changing students grade: {e}")
        conn.rollback()

    # vyber ktore kurzy chce odstranit
    if len(output_courses) == 0:
        print("Tento učiteľ nemá priradený žiadny kurz!")
        return

    chosed_courses = []
    while True:
        count_co = 0
        all_courses_id = []
        print(f"Already chosen courses {chosed_courses}")
        for course in output_courses:
            print(f"[{count_co}] {course['name']}")
            all_courses_id.append(course['course_id'])
            count_co += 1
        while True:
            print("Choose a course to be removed: ")
            vysl = input_number_from_to(-1, count_co-1)
            if vysl not in chosed_courses:
                break
            else:
                print("You already chose this course!")
        if vysl == -1:
            break
        chosed_courses.append(vysl)

    # ziskanie ID vybranych kurzov
    final_courses_id = []
    for kurz in chosed_courses:
        final_courses_id.append(all_courses_id[kurz])

    # vymazanie kurzu od ucitela
    for course in final_courses_id:
        try:
            sql_command = sql.SQL(
                """
                UPDATE courses
                SET teacher_id = null
                WHERE course_id = {}
                """
            ).format(
                sql.Literal(course)
            )
            cur.execute(sql_command)
            conn.commit()
        except Exception as e:
            print(f"ERROR removing teachers course: {e}")
            conn.rollback()
    print(GREEN + "Successfully removed teachers course!" + RESET)
    print("*****************************")


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


def list_courses(conn, cur, table):
    print(f"List of {table}: ")
    try:
        joined_tables = join_tables_curses_teachers(conn, cur)

        students_list = []
        for row in joined_tables:
            print(f"Subject: {row['nazov_kurzu']}")
            print(f"    Teacher: {row['meno_ucitela']} {row['priezvisko_ucitela']}")
            spojovacia_tabulka = vytvor_spojovaciu_tabulku(conn, cur)
            for row_ST in spojovacia_tabulka:
                if row_ST['nazov_kurzu'] == row['nazov_kurzu']:
                    students_list.append(f"{row_ST['meno_ziaka']} {row_ST['surname']}")

            students_string = ", ".join(students_list)
            print(f"    Students: {students_string}")
            students_list = []
        print("*****************************")
        print("Lists without any teacher: ")
        try:
            sql_command = sql.SQL(
                """
                SELECT *
                FROM courses
                WHERE teacher_id IS null
                """
            )
            cur.execute(sql_command)
            output_empty_courses = cur.fetchall()
        except Exception as e:
            print(f"ERROR changing students grade: {e}")
            conn.rollback()

        if len(output_empty_courses) == 0:
            print("There are no courses without teacher!")
            return

        for empty_course in output_empty_courses:
            print(f"Subject: {empty_course['name']}")
            print(f"    Teacher: None")
        print("*****************************")

    except Exception as e:
        print(f"Chyba pri listovaní tabuľky kurov: {e}")
        conn.rollback()


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
