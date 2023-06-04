import mysql.connector
import os
import datetime


def dump(cur):

    # Data for Saving
    data = ""

    # Getting all table names
    cur.execute('SHOW TABLES;')
    tables = []
    for record in cur.fetchall():
        tables.append(record[0])

    for table in tables:
        cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
        data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

    # Setting for saving db
    now = datetime.datetime.now()
    filename = str("tmpfile" + ".sql")

    file = open(filename, "w")
    file.writelines(data)
    file.close()

    print("Successfully dump " + filename)

    return filename


#dump(user_cursor)
