import csv
import sqlite3

def setup_database():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        # Create the table with an ID and message column
        c.execute('''
        CREATE TABLE IF NOT EXISTS customer_messages 
            (id INTEGER PRIMARY KEY, 
             message TEXT, 
             replied INTEGER DEFAULT 0)
        ''')

def insert_csv_to_db():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        with open('customer_messages.csv', mode ='r') as file:
            csvFile = csv.reader(file)
            next(csvFile)  # Skip the header row
            
            for row in csvFile:
                user_id = row[0]       # User ID column
                message_body = row[2]  # Message Body column

                # Insert only if the user ID doesn't already exist in the table for simplicity
                # (This avoids repeated insertion of messages from the same user)
                c.execute('SELECT id FROM customer_messages WHERE id = ?', (user_id,))
                if not c.fetchone():
                    c.execute('INSERT INTO customer_messages (id, message) VALUES (?, ?)', (user_id, message_body))

if __name__ == "__main__":
    setup_database()
    insert_csv_to_db()
