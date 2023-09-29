import csv
import sqlite3

def insert_csv_to_db():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        with open('customer_messages.csv', mode ='r') as file:
            csvFile = csv.reader(file)
            for row in csvFile:
                message = row[0]
                c.execute('SELECT id FROM customer_messages WHERE message = ?', (message,))
                if not c.fetchone():
                    c.execute('INSERT INTO customer_messages (message) VALUES (?)', (message,))

if __name__ == "__main__":
    insert_csv_to_db()
