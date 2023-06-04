import mysql.connector


if __name__ == '__main__':
    connection1 = mysql.connector.connect(
        user='root', password='mypassword', host='mysql', port="3306", database='vcdb')  
    print("DB connected")
    cursor = connection1.cursor()
    cursor.execute('show tables;')
    students = cursor.fetchall()
    print(students)

    connection2 = mysql.connector.connect(
        user='root', password='mypassword', host='mysql', port="3306", database='userdb')  #壹定要用root為user to 33062
    cursor = connection2.cursor()
    cursor.execute('show tables;')
    alls = cursor.fetchall()
    print(alls)

    connection1.close()
    connection2.close()