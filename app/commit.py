import mysql.connector as m
import uuid
import os
import datetime
from dump import dump
from diff import get_diff
import globals

def commit(msg):  # use globals
    
    # get 目前 user 的相關資訊
    query = "SELECT * FROM user WHERE uid = '%s';" % globals.current_uid
    globals.vc_cursor.execute(query)
    userInfo = globals.vc_cursor.fetchone()
    
    # get 目前 branch 的相關資訊
    query = "SELECT * FROM branch WHERE bid = '%s'" % globals.current_bid
    globals.vc_cursor.execute(query)
    branchInfo = globals.vc_cursor.fetchone()
    
    # check if user can commit or not
    if (userInfo[3] != None):  # user 有 commit 過
        userNode = userInfo[3]
        branchTail = branchInfo[2]
    
        if (userNode != branchTail):
            print("Please update to the newest version of the branch first!")
            return
        
    elif (userInfo[3] == None and branchInfo[2] != None):  # user 沒有 commit 過 但該 branch 有紀錄
        print("Please update to the newest version of the branch first!")
        return
        
    
    # dump
    path = "./branch_tail_schema"
    newSQL = dump(globals.user_cursor)  # return file name
    oldSQL = str(branchInfo[1]) + '.sql'  # exist branchName.sql if the branch has been commited before
    
    # diff
    if (branchInfo[2] != None):  # 該 branch 有紀錄
        upgrade = get_diff(os.path.join(path, oldSQL), os.path.join(path, newSQL))
        downgrade = get_diff(os.path.join(path, newSQL), os.path.join(path, oldSQL)) 
    else:
        upgrade = get_diff(None, os.path.join(path, newSQL))
        downgrade = get_diff(os.path.join(path, newSQL), None)

    # check if upgrade = nothing
    if (upgrade == ""):
        os.remove(os.path.join(path, newSQL))
        print("Nothing to commit")
        return
    
    
    # update commit table
    version = str(uuid.uuid4())[:8]  # uuid (八位數的亂數)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if (branchInfo[2] != None):
        insert = "INSERT INTO commit (version, bid, last_version, upgrade, downgrade, time, uid, msg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        last_version = branchTail
        val = (version, globals.current_bid, last_version, upgrade, downgrade, time, globals.current_uid, msg)
    else:
        insert = "INSERT INTO commit (version, bid, upgrade, downgrade, time, uid, msg) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (version, globals.current_bid, upgrade, downgrade, time, globals.current_uid, msg)
    
    globals.vc_cursor.execute(insert, val)
    
    # update branch table
    update = "UPDATE branch SET tail = (%s) WHERE bid = (%s);"
    val = (version, globals.current_bid)  # tail 記錄 version
    globals.vc_cursor.execute(update, val)
    
    # update user table
    update = "UPDATE user SET current_version = (%s), current_bid = (%s) WHERE uid = (%s);"
    val = (version, globals.current_bid, globals.current_uid)
    globals.vc_cursor.execute(update, val)
    
    
    # delete old dump file and rename new dump file
    if (os.path.exists(os.path.join(path, oldSQL))):
        os.remove(os.path.join(path, oldSQL))
    os.rename(os.path.join(path, newSQL), os.path.join(path, oldSQL))
    
    print("Successfully commit")
    globals.vc_connect.commit()

    return version
    
if __name__ == '__main__':
    msg = "commit"
    commit(msg)