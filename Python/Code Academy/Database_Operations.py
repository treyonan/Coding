# SQL Lite ----------------------

# Create table and insert a single row --------------------

from start import helper
helper()
import sqlite3

con = sqlite3.connect("titanic.db")
curs = con.cursor()

# Create table named new_table
curs.execute('''CREATE TABLE new_table (
                   name TEXT,
                   age INTEGER,
                   username TEXT,
                   pay_rate REAL)''')

# Insert row of values into new_table
curs.execute('''INSERT INTO new_table VALUES ('Bob Peterson',
34, 'bob1234', 40.00)''')


# Insert multiple rows ----------------------------------------------

from start import helper
helper()
import sqlite3

con = sqlite3.connect("titanic.db")
curs = con.cursor()

# Here is the new_rows object
new_rows = [('Anne Smith', 33, 'AS896', 25.00),
            ('Billy Roberts', 29, 'bill5Rob', 30.00),
            ('Jason Johnson', 48, 'JasonJ77', 40.00),
            ('Tim Trunk', 51, 'Timtrunk4', 40.00),
            ('Sarah Fall',19, 'SFall232', 25.00)
            ]

# Insert new_rows into the new_table table
curs.executemany('''INSERT INTO new_table VALUES (?,?,?,?)''', new_rows)

# Retrieving Data -------------------------------------------------------------

import sqlite3

con = sqlite3.connect("titanic.db")
curs = con.cursor()

# Pull the first row from the titanice data table (print to view output)
one = curs.execute("SELECT * FROM titanic").fetchone()
print(one)

# Pull the first ten rows from the titanice data table (print to view output)
ten = curs.execute("SELECT * FROM titanic").fetchmany(10)
print(ten)

# Pull every row from the titanice data table (print to view output)
all_rows = curs.execute("SELECT * FROM titanic").fetchall()
print(all_rows)

# Pull every row from the titanice data table for those who survived (print to view output)
all_survived = curs.execute('''SELECT * FROM titanic WHERE Survived = 1;''').fetchall()
print(all_survived)



