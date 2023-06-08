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
import dump
import diff
import globals
import sys

# function
def checkout(newBranchName, isNewBranchOrNot):
    print("start checking out.")

    # get user's current branch name.
    # assume userid is global variable
    query = "SELECT current_bid FROM vcdb.user where uid = %s;"
    globals.vc_cursor.execute(query, [globals.current_uid])
    currentBranchID = globals.vc_cursor.fetchone()[0]

    # store current branche name
    query = f"SELECT name FROM vcdb.branch where bid = {currentBranchID};"
    globals.vc_cursor.execute(query)
    currentBranchName = globals.vc_cursor.fetchone()[0]

    try:
        if isNewBranchOrNot == "No":
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            globals.vc_cursor.execute(query)
            allBranchNames = globals.vc_cursor.fetchall()
            allBranchNames = ["%s" % x for x in allBranchNames]
            if newBranchName not in allBranchNames:
                print("The specified branch name does not exists.")
                return "The specified branch name does not exists."

            # check if tail == current schema
            # dump current userdb's schema
            fileName = dump.dump(globals.user_cursor)

            result = diff.get_diff(f"./branch_tail_schema/{fileName}", f"./branch_tail_schema/{currentBranchName}.sql")

            if result != "":
                print("Please commit before checking out to another branch.")
                return "Please commit before checking out to another branch."
            # directly change userdb's schema: drop whole schema + import newBranch schema to it
            query = f"drop schema {globals.userdb_name};"
            globals.user_cursor.execute(query)
            targetBranchTailCommands = diff.read_sql_file(f"./branch_tail_schema/{newBranchName}.sql")
            globals.user_cursor.execute(f"create database {globals.userdb_name};")
            globals.user_cursor.execute(f"use {globals.userdb_name};")
            for statement in targetBranchTailCommands.split(';'):
                if len(statement.strip()) > 0:
                    globals.user_cursor.execute(statement + ';')
            
            # delete tmp file
            os.remove(f"./branch_tail_schema/{fileName}")
            
        else:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            globals.vc_cursor.execute(query)
            allBranchNames = globals.vc_cursor.fetchall()
            allBranchNames = ["%s" % x for x in allBranchNames]
            if newBranchName in allBranchNames:
                print("Please create a branch name that is not identical to the existing ones.")
                return "Please create a branch name that is not identical to the existing ones."

            # update branch table: add new branch 
            globals.vc_cursor.execute("use vcdb;")       
            query = "insert into branch (name, tail) values(%s, %s);"
            globals.vc_cursor.execute(query, [newBranchName, ""])
            globals.vc_connect.commit()


        # update user table: current_bid, current_version
        globals.vc_cursor.execute("use vcdb;")
        query = "SELECT bid, tail FROM vcdb.branch where name = %s;"
        globals.vc_cursor.execute(query, [newBranchName])
        result = globals.vc_cursor.fetchall()[0]
        print(result)
        if type(result) == int:
            newBranchID = result
            newTail = ""
        else:
            newBranchID, newTail = result

        globals.vc_cursor.execute("use vcdb;")
        query = "UPDATE user SET current_bid=%s, current_version=%s WHERE uid = %s;"
        globals.vc_cursor.execute(query, [newBranchID, newTail, globals.current_uid])
        globals.vc_connect.commit()

        # update global variables: current_bid
        globals.current_bid = newBranchID

        # lastly: create a newBranchName sql file in branch_tail_schema
        if isNewBranchOrNot != "No":
            file = open(f"./branch_tail_schema/{newBranchName}.sql","w")
            file.writelines("")
            file.close()
        

        #print success message
        print(f"Successfully checked out to branch {newBranchName}.")
        return f"Successfully checked out to branch {newBranchName}."

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("============================================")
        print("Error file name: ", fname)
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")

# checkout("func2", False)