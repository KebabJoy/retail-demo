import sqlite3

conn = sqlite3.connect('actions/example.db')

c = conn.cursor()
# c.execute('''CREATE TABLE seller_requests (id INTEGER, reviewed BOOLEAN, user_id INTEGER, PRIMARY KEY(id ASC), FOREIGN KEY (user_id) REFERENCES users(id))''')
# c.execute('''CREATE TABLE roles (id INTEGER, name VARCHAR(255), PRIMARY KEY(id ASC))''')
# c.execute('''INSERT INTO roles (name) VALUES('client')''')
# c.execute('''INSERT INTO roles (name) VALUES('seller')''')
# c.execute('''INSERT INTO roles (name) VALUES('admin')''')
# c.execute('''CREATE TABLE users (id INTEGER, name VARCHAR(255), email TEXT, role_id INTEGER, FOREIGN KEY (role_id) REFERENCES roles(id), PRIMARY KEY(id ASC))''')

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')


# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# # Create table
# c.execute('''CREATE TABLE orders
#              (order_date, order_number, order_email, color, size, status)''')
#
# c.execute('''DROP TABLE reviews''')
# c.execute('''CREATE TABLE reviews (text text, email VARCHAR(255))''')
#
# # # data to be added
# purchases = [('2006-01-05', 123456, 'example@rasa.com', 'blue', 9, 'shipped'),
#              ('2021-01-05', 123457, 'me@rasa.com', 'black', 10, 'order pending'),
#              ('2021-01-05', 123458, 'me@gmail.com', 'gray', 11, 'delivered'),
#              ]
#
# # add data
# c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)
#
# # AVAILABLE INVENTORY
# # Create table
# c.execute('''CREATE TABLE inventory
#              (size, color)''')
#
# # data to be added
# inventory = [(7, 'blue'),
#              (8, 'blue'),
#              (9, 'blue'),
#              (10, 'blue'),
#              (11, 'blue'),
#              (12, 'blue'),
#              (7, 'black'),
#              (8, 'black'),
#              (9, 'black'),
#              (10, 'black')
#              ]
#
# # add data
# c.executemany('INSERT INTO inventory VALUES (?,?)', inventory)

# Save (commit) the changes
conn.commit()

# end connection
conn.close()
