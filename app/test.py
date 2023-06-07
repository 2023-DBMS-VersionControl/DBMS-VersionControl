# this file is a GUI.py mock-up, aiming at testing whether the function.py is going to work in GUI.py using all global variables.

# import globals
from checkout import checkout
import mysql.connector
import globals
import os
from dotenv import load_dotenv
load_dotenv()

def init_connections():
    print("start initing connections.")

    # get 2 connections
    user = os.getenv("MYSQL_USER")
    pwd = os.getenv("MYSQL_PASSWORD")

    connection1 = mysql.connector.connect(
        user=user, password=pwd, host='127.0.0.1', port="3306", database='vcdb')
    # globals.connection1 = connection1
    # globals.vc_cursor = connection1.cursor()
    print("VCDB connected.")

    connection2 = mysql.connector.connect(
        user=user, password=pwd, host='127.0.0.1', port="3306", database='userdb')
    # globals.connection2 = connection2
    # globals.user_cursor = connection2.cursor()
    print("user DB connected.")

    connection3 = mysql.connector.connect(
        user="root", password="mypassword", host='140.112.106.237', port="16919", database='vcdb')
    # globals.connection2 = connection2
    # globals.user_cursor = connection2.cursor()
    print("lab DB connected.")

    # insert data for testing
    # query = "insert into user values (%s, %s, %s, %s, %s);"
    # values = ["test2", "aMember", "member.com", "testtt2", "func2"]
    # globals.vc_cursor.execute(query, values)
    # globals.connection2.commit()
    # globals.userid = "test2"

    # print(globals.connection1, globals.vc_cursor, globals.user_cursor)
    return


init_connections()

# test functions
# checkout("func1", False)
# checkout("func3", False)
# checkout("func3", True)
