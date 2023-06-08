import mysql.connector
import create
import sys
import globals
import uuid

# def init(user, pwd, host, port, database_name):

#     # set DB connection
#     global vc_connect
#     global vc_cursor
#     global user_connect
#     global user_cursor
#     try:
#         user_connect = mysql.connector.connect(host=host, database=database_name, user=user, passwd=pwd)
#         user_cursor = user_connect.cursor()

#         # create vcdb
#         user_cursor.execute("CREATE DATABASE IF NOT EXISTS vcdb")
#         user_connect.commit()
#         # create table in DBVC
#         create.create(user, pwd, host, port)
#         vc_connect  = mysql.connector.connect(host=host, database="vcdb", user=user, passwd=pwd)
#         vc_cursor = vc_connect.cursor()
#         vc_cursor.execute("USE vcdb")
#         vc_cursor.execute(f"INSERT INTO branch (name) VALUES ('main')")
#         vc_connect.commit()

#         print("Im init")

#         return vc_connect, vc_cursor, user_connect, user_cursor
    
#     except Exception as e:
#         print(e)
#         print("Im init")
#         return None
    
def init(user, pwd, host, port, database_name):

    # set DB connection
    try:
        # store user db connection info
        user_connect = mysql.connector.connect(host=host, database=database_name, user=user, passwd=pwd)
        user_cursor = user_connect.cursor()
        globals.user_connect = user_connect
        globals.user_cursor = user_cursor

        # create vcdb
        user_cursor.execute("CREATE DATABASE IF NOT EXISTS vcdb;")
        user_connect.commit()
        # create table in DBVC
        create.create(user, pwd, host, port)
        vc_connect  = mysql.connector.connect(host=host, database="vcdb", user=user, passwd=pwd)
        vc_cursor = vc_connect.cursor()
        globals.vc_connect = vc_connect
        globals.vc_cursor = vc_cursor
        vc_cursor.execute("USE vcdb;")
        vc_cursor.execute(f"INSERT INTO branch (name) VALUES ('main');")
        vc_connect.commit()
        print("Im init")
        return
    
    except:
    # except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("============================================")
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")
        # print(e)
        # print("Im init")
        # return None
        return

def register(user_name, user_email):
    try:
        # create uuid
        user_uuid = str(uuid.uuid4())

        #Update user table
        print("=============== into register function ==============")
        print(globals.vc_cursor)
        globals.vc_cursor.execute("USE vcdb;")
        globals.vc_cursor.execute(f"INSERT INTO user (uid, name, email, current_bid) VALUES ('{user_uuid}', '{user_name}', '{user_email}', '1');")
        globals.vc_connect.commit()
        globals.vc_cursor.execute("select bid from branch where name = 'main';")
        result = globals.vc_cursor.fetchone()
        print("===============")
        print(result)
        globals.current_bid = result
        print("Successfully registered.")
        return
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("============================================")
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")
        return

def login(user, pwd, host,  database_name, user_name, user_email):
    # set DB connection
    # global vc_connect
    # global vc_cursor
    # global user_connect
    # global user_cursor

    #set current_version and brench
    # global current_uid
    # global current_version
    # global current_bid

    #get user's version and branch
    try:
        user_connect = mysql.connector.connect(host=host, database=database_name, user=user, passwd=pwd)
        user_cursor = user_connect.cursor()

        globals.user_connect = user_connect
        globals.user_cursor = user_cursor

        # create vcdb
        vc_connect  = mysql.connector.connect(host=host, database="vcdb", user=user, passwd=pwd)
        vc_cursor = vc_connect.cursor()
        globals.vc_connect = vc_connect
        globals.vc_cursor = vc_cursor

        vc_cursor.execute("USE vcdb")
        vc_cursor.execute(f"select uid, current_version, current_bid from user where name = '{user_name}' AND email = '{user_email}'")
        result = vc_cursor.fetchone()
        current_uid, current_version, current_bid = result

        globals.current_uid = current_uid
        globals.current_version = current_version
        globals.current_bid = current_bid
        # db_cursor.execute(f"select bid from branch where name = '{user_name}' AND email = '{user_email}'")

        return 

    except Exception as e:
        print(e)
        return None
    
def log():
    try:
        print("=============== into log function ==============")
        print(globals.vc_cursor)
        globals.vc_cursor.execute("USE vcdb;")
        globals.vc_cursor.execute(f"select name, version, time, uid, msg from branch, commit where branch.bid = commit.bid and commit.bid = '{globals.current_bid}';")
        result = globals.vc_cursor.fetchall()
        current_branch_name = result
        globals.current_branch_name = current_branch_name
        print("===============")
        print(result)
        print("Log Successfully.")
        return result
    
    except Exception as e:
        return("Log error: ",e)

def getBnameFromBid():
    try:
        print("=============== into getBnameFromBid function ==============")
        print(globals.vc_cursor)
        globals.vc_cursor.execute("USE vcdb;")
        globals.vc_cursor.execute(f"select name from branch where branch.bid = '{globals.current_bid}';")
        result = globals.vc_cursor.fetchone()[0]
        print("===============")
        print(result)
        current_branch_name = result
        globals.current_branch_name = current_branch_name
        print("Get Bname Successfully.")
        return
    
    except Exception as e:
        return("Get error: ",e)