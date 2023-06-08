import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import globals
import sys
import os


# remote vcdb info
vcdb_user = os.getenv("VCDB_USER")
vcdb_pwd = os.getenv("VCDB_PWD")
vcdb_host = os.getenv("VCDB_HOST")
vcdb_port = os.getenv("VCDB_PORT")

def create():
    try:
        vc_connect = mysql.connector.connect(
            user=vcdb_user, password=vcdb_pwd, host=vcdb_host, port=vcdb_port)

        vc_cursor = vc_connect.cursor()
        vc_cursor.execute("CREATE DATABASE IF NOT EXISTS vcdb;")
        vc_connect.commit()

        globals.vc_connect = vc_connect
        globals.vc_cursor = vc_cursor
        vc_cursor.execute("USE vcdb;")


        # creating tables for vcdb: branch, commit, user, merge
        creating_table = '''CREATE TABLE IF NOT EXISTS branch(
            bid int not null AUTO_INCREMENT,
            name varchar(125) not null,
            tail varchar(500),
            PRIMARY KEY (bid));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()
        vc_cursor.execute(f"INSERT INTO branch (name) VALUES ('main');")
        vc_connect.commit()


        creating_table = '''CREATE TABLE IF NOT EXISTS commit(
            version varchar(500) not null,
            bid int not null,
            last_version varchar(500),
            upgrade varchar(5000) not null,
            downgrade varchar(5000) not null,
            time datetime not null,
            uid varchar(500) not null,
            msg varchar(500),
            PRIMARY KEY (version));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()


        creating_table = '''CREATE TABLE IF NOT EXISTS user(
            uid varchar(500) not null,
            name varchar(125) not null,
            email varchar(125) not null,
            current_version varchar(500),
            current_bid int not null,
            PRIMARY KEY (uid),
            CONSTRAINT FK_UserBranch FOREIGN KEY (current_bid)
            REFERENCES branch(bid));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()


        creating_table = '''CREATE TABLE IF NOT EXISTS merge(
            merged_version varchar(500) not null,
            main_branch_version varchar(500) not null,
            target_branch_version varchar(500) not null,
            PRIMARY KEY (merged_version),
            CONSTRAINT FK_MergeCommit1 FOREIGN KEY (merged_version)
            REFERENCES commit(version),
            CONSTRAINT FK_MergeCommit2 FOREIGN KEY (main_branch_version)
            REFERENCES commit(version),
            CONSTRAINT FK_MergeCommit3 FOREIGN KEY (target_branch_version)
            REFERENCES commit(version));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()

        vc_cursor.execute('show tables;')
        vc_alltables = vc_cursor.fetchall()
        print("Successfully created vcdb & tables.")
    
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("============================================")
        print("Error file name: ", fname)
        print("Error Type: ", exc_type)
        print("Error occurs in line:", exc_tb.tb_lineno)
        print("Error msg:", exc_obj)
        print("============================================")