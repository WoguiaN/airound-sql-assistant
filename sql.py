import sqlite3 

## connect to sqlite 

connection = sqlite3.connect("student.db")

## create a cursor object to insert record, create table, retrieve 

cursor = connection.cursor()

## create a table 
table_info="""
Create table STUDENT(
NAME VARCHAR(25),
CLASS VARCHAR(25),
SECTION VARCHAR(25), 
MARKS INT);

"""

cursor.execute(table_info)

##insert Some records 

cursor.execute("insert into Student values('Krish', 'Data Science','A', 90)")
cursor.execute("insert into Student values('John', 'Computer Science', 'A', 88)")
cursor.execute("insert into Student values('Alice', 'Mathematics', 'B', 76)")
cursor.execute("insert into Student values('Michael', 'Physics', 'A', 91)")
cursor.execute("insert into Student values('Emma', 'Data Science', 'A', 95)")
cursor.execute("insert into Student values('David', 'Statistics', 'B', 82)")
cursor.execute("insert into Student values('Sophia', 'Computer Science', 'A', 89)")
cursor.execute("insert into Student values('Daniel', 'Artificial Intelligence', 'A', 93)")
cursor.execute("insert into Student values('Olivia', 'Mathematics', 'B', 78)")
cursor.execute("insert into Student values('James', 'Data Science', 'A', 87)")
cursor.execute("insert into Student values('Lucas', 'Machine Learning', 'A', 92)")

##Display all the records 
print("The inserted records are :")

data = cursor.execute("select * from STUDENT")

for row in data :
    print(row)

## Close the connection after lecture 
connection.commit()
connection.close()