from distlib.compat import raw_input
from WorkWithDB import WorkWithDB

print('1. Select books. \n')
print('2. Insert new book. \n')
print('3. Insert new list of books. \n')
print('4. Edit book by id. \n')
print('5. Edit multi books by id. \n')
print('6. Delete book by id. \n')

work = raw_input('Enter your work: ')
print('\n')

db = WorkWithDB()
params = ""

if work == '1':
    sql = "SELECT * FROM books"
    db.select(sql)

elif work == '2':
    sql = "INSERT INTO books(name, author) VALUES (%s, %s)"
    params = ("HELLO", "TEST123")
    db.insert(sql, params)

elif work == '3':
    sql = "INSERT INTO books(name, author) VALUES (%s, %s)"
    params = [("PYTHON", "PYTHON1"),
              ("MACHINE LEARNING", "ANDREW NG")]
    db.insert_list(sql, params)

elif work == '4':
    sql = "UPDATE books SET name = %s, author = %s WHERE id = %s "
    params = ("DEEP LEARNING", "DEEP LEARNING 123", 7)
    db.update(sql, params)

elif work == '5':
    sql = "UPDATE books SET name = %s, author = %s WHERE id = %s "
    params = [("Python can ban", "python", 5),
              ("Machine Learning can ban", "Vu Huu Tiep", 6),
              ("Deep Learning", "Deep Learning", 7)]
    db.update_list(sql, params)

elif work == '6':
    params = 7
    sql = "DELETE FROM books WHERE id = " + str(params)
    db.delete(sql)

db.close_connect()
