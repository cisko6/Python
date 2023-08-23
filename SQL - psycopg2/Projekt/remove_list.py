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
        joined_tables = join_tables_curses_teachers(conn,cur)

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


















