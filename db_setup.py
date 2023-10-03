import csv
import sqlite3
def setup_database():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        # Create the customer_messages table
        c.execute('''
        CREATE TABLE IF NOT EXISTS customer_messages 
            (id INTEGER PRIMARY KEY,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, message TEXT, replied BOOLEAN DEFAULT FALSE)
        ''')
        
        # Modify the agents table structure here
        c.execute('''
        CREATE TABLE IF NOT EXISTS agents 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)
        ''')
        
        # Create the message_assignments table
        c.execute('''
        CREATE TABLE IF NOT EXISTS message_assignments 
            (id INTEGER PRIMARY KEY, message_id INTEGER, agent_id INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES customer_messages (id),
            FOREIGN KEY (agent_id) REFERENCES agents (id))
        ''')

def insert_csv_to_db():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        with open('customer_messages.csv', mode ='r') as file:
            csvFile = csv.reader(file)
            next(csvFile)  # Skip the header row
            
            for row in csvFile:
                user_id = row[0]       # User ID column
                time_stamp = row[1]    # Timestamp column
                message_body = row[2]  # Message Body column

                # Insert only if the user ID doesn't already exist in the table for simplicity
                # (This avoids repeated insertion of messages from the same user)
                c.execute('SELECT id FROM customer_messages WHERE id = ?', (user_id,))
                if not c.fetchone():
                    c.execute('INSERT INTO customer_messages (id, timestamp, message) VALUES (?, ?, ?)', (user_id, time_stamp, message_body))
                    
def divide_replies_among_agents():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()

        # Fetch all agents
        c.execute('SELECT id FROM agents')
        agent_ids = [item[0] for item in c.fetchall()]

        # Fetch all replied messages that aren't yet assigned
       # c.execute('''
        #    SELECT id FROM customer_messages WHERE id IN (SELECT message_id FROM replies) 
         #   AND id NOT IN (SELECT message_id FROM message_assignments)
        #''')
        c.execute('''
            SELECT id FROM customer_messages WHERE id NOT IN (SELECT message_id FROM message_assignments)
        ''')
        message_ids = [item[0] for item in c.fetchall()]

        # If there are no agents or no messages, just return
        if not agent_ids or not message_ids:
            return

        # Distribute the messages amongst the agents
        for index, message_id in enumerate(message_ids):
            agent_id = agent_ids[index % len(agent_ids)]  # Cycle through the agent list
            c.execute('INSERT INTO message_assignments (message_id, agent_id, timestamp) VALUES (?, ?, datetime("now"))', (message_id, agent_id))
        
        conn.commit()    

if __name__ == "__main__":
    setup_database()
    insert_csv_to_db()
    divide_replies_among_agents()
