# 到時候替換成品歷的init.py


# import packages
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
import back.checkout as checkout2


# main file
app = Flask(__name__)
CORS(app)

connection1 = mysql.connector.connect(
    user="root", password="mypassword", host='mysql', port="3306", database='vcdb')  
print("DB connected.")
vc_cursor = connection1.cursor()
vc_cursor.execute('show tables;')
students = vc_cursor.fetchall()
print(students)

connection2 = mysql.connector.connect(
    user="root", password="mypassword", host='mysql', port="3306", database='userdb')  
user_cursor = connection2.cursor()
user_cursor.execute('show tables;')
alls = user_cursor.fetchall()
print(alls)





# #####################################################################
# @app.route('/', methods=["GET", "POST"])
# def index():
#     return "Welcome."



# @app.route('/checkout', methods=['GET'])
# def checkout():
#     global vc_cursor
#     result = checkout2.checkout(vc_cursor, "func1", False)
#     return jsonify({'return': str(result)})


# if __name__ == '__main__':
#     print("HI!")
#     app.run(host='0.0.0.0', port=5001, debug=True)