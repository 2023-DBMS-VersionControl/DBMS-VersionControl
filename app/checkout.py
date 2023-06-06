# description
# 1. new == False:
#     update user table
#     check if tail == current schema
#     if not: warn, exit
#     directly change userdb's schema: drop + create
# 2. new == True:
#     update user table
#     since creating new branch does not require a commit, we don't update branch table


import os
import mysql.connector
import dump
import diff
import globals
import sys


# function
def checkout(newBranchName, new=False):
    print("start checking out.")

    # get user's current branch name.
    # assume userid is global variable
    query = "SELECT current_branch FROM vcdb.user where uid = %s;"
    globals.vc_cursor.execute(query, [globals.userid])
    currentBranchName = globals.vc_cursor.fetchone()[0]
    print(currentBranchName)
    
    try:
        if new == False:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            globals.vc_cursor.execute(query)
            allBranchNames = globals.vc_cursor.fetchall()
            allBranchNames = ["%s" % x for x in allBranchNames]
            if newBranchName not in allBranchNames:
                print("The specified branch name does not exists.")
                return

            # check if tail == current schema
            # dump current userdb's schema
            fileName = dump.dump(globals.user_cursor)
            # check differences
            userCurrentSchema = diff.read_sql_file(f"./{fileName}.sql")
            currentBranchTail = diff.read_sql_file(f"../branch_tail_schema/{currentBranchName}.sql")
            result = diff.get_diff(currentBranchTail, userCurrentSchema)
            if result != "":
                print("Please commit before checking out to another branch.")
                return
            # directly change userdb's schema: drop whole schema + import newBranch schema to it
            query = 'drop schema userdb;'
            globals.user_cursor.execute(query)
            targetBranchTailCommands = diff.read_sql_file(f"../branch_tail_schema/{newBranchName}.sql")
            globals.user_cursor.execute("create database userdb;")
            globals.user_cursor.execute("use userdb;")
            for statement in targetBranchTailCommands.split(';'):
                if len(statement.strip()) > 0:
                    globals.user_cursor.execute(statement + ';')
            # update user table: current_branch, current_version
            # if checking out to an existing branch, the user will be on the latest commit of the target branch
            query = "SELECT tail FROM vcdb.branch where name = %s;"
            globals.vc_cursor.execute(query, [newBranchName])
            newBranchTail = globals.vc_cursor.fetchone()[0]
            globals.vc_cursor.execute("use vcdb;")
            query = "UPDATE user SET current_branch=%s, current_version=%s WHERE uid = %s;"
            globals.vc_cursor.execute(query, [newBranchName, newBranchTail, "testtt"])
            globals.connection1.commit()
            # delete tmpfile.sql
            os.remove("tmpfile.sql")

        else:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            globals.vc_cursor.execute(query)
            allBranchNames = globals.vc_cursor.fetchall()
            allBranchNames = ["%s" % x for x in allBranchNames]
            if newBranchName in allBranchNames:
                print("Please create a branch name that is not identical to the existing ones.")
                return

            # update branch table
            globals.vc_cursor.execute("use vcdb;")       
            query = "insert into `branch` (name, tail) values(%s, %s);"
            globals.vc_cursor.execute(query, [newBranchName, " "])
            globals.connection1.commit()


        #update user table: current_branch, current_version
        globals.vc_cursor.execute("use vcdb;")
        query = "UPDATE user SET current_branch = %s WHERE uid = %s;"
        globals.vc_cursor.execute(query, [newBranchName, "testtt"])
        globals.connection1.commit()
        query = "UPDATE `user` SET current_branch = %s WHERE uid = %s;"
        globals.vc_cursor.execute(query, [newBranchName, "testtt"])
        globals.connection1.commit()

        #print success message
        print(f"Successfully checked out to branch {newBranchName}.")
        return

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("============================================")
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")


# checkout("func2", False)
