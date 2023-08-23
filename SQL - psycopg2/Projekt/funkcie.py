from psycopg2 import sql
import sys


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











def join_tables_curses_teachers(conn,cur):
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




def vstupy_ziaka():
    #name, surname, grade
    vysl = []
    print("Enter students name: ", end='')
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