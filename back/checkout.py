# description
# 1. new == False:
    # update user table
    # check if tail == current schema
    # if not: warn, exit
    # directly change userdb's schema: drop + create
# 2. new == True:
    # update user table
    # since creating new branch does not require a commit, we don't update branch table


# import packages
import os
import mysql.connector
import dump
import diff


# function
def checkout(newBranchName, new=False):
    print("start checking out.")
    connection1 = mysql.connector.connect(
        user="root", password="tubecity0212E_", host='127.0.0.1', port="3306", database='vcdb')
    print("VCDB connected.")
    vc_cursor = connection1.cursor()

    connection2 = mysql.connector.connect(
    user="root", password="tubecity0212E_", host='127.0.0.1', port="3306", database='userdb')
    print("user DB connected.")
    user_cursor = connection2.cursor()

    # get user's current branch name.
    # assume userid is global variable
    query = "SELECT current_branch FROM vcdb.user where uid = %s;"
    vc_cursor.execute(query, ["testtt"])
    currentBranchName = vc_cursor.fetchone()[0]
    
    try:
        if new == False:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            vc_cursor.execute(query)
            allBranchNames = vc_cursor.fetchall()
            allBranchNames = ["%s" % x for x in allBranchNames]
            if newBranchName not in allBranchNames:
                print("The specified branch name does not exists.")
                return

            # check if tail == current schema
            # dump current userdb's schema
            dump.dump(user_cursor)
            # check differences
            userCurrentSchema = diff.readSqlFile(f"./tmpfile.sql")
            currentBranchTail = diff.readSqlFile(f"./branch_tail_schema/{currentBranchName}.sql")
            result = diff.get_diff(userCurrentSchema, currentBranchTail)
            print("======================================================")
            print(result)


        else:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            vc_cursor.execute(query)
            allBranchNames = vc_cursor.fetchall()
            allBranchNames = ["%s" % x for x in allBranchNames]
            if newBranchName in allBranchNames:
                print("Please create a branch name that is not identical to the existing ones.")


        # update user table
        query = "UPDATE user SET current_branch = (%s) WHERE uid = %s;"
        vc_cursor.execute(query, [newBranchName, ["testtt"]])


        # print success message
        print("Successfully checked out to branch {newBranchName}.")
        connection1.close()
        connection2.close()
        return

    except Exception as e:
        print(e)


checkout("func1", False)
