from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import bcrypt
import sqlite3

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'bellababu'
Session(app)

# Initialize DB
def init_db():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS customer_messages
                     (id INTEGER PRIMARY KEY,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, message TEXT, replied BOOLEAN DEFAULT FALSE)''')
        c.execute('''CREATE TABLE IF NOT EXISTS replies
                     (id INTEGER PRIMARY KEY, message_id INTEGER , reply TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS agents (id INTEGER PRIMARY KEY,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL )''')
        c.execute('''CREATE TABLE IF NOT EXISTS message_assignments (id INTEGER PRIMARY KEY, message_id INTEGER , agent_id INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (message_id) REFERENCES customer_messages (id),FOREIGN KEY (agent_id) REFERENCES agents (id))''')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    customer_id = request.form.get('customer_id')
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO customer_messages (id,message) VALUES (?,?)', (customer_id,message,))
        flash('Message sent successfully!')
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    search_id = request.form.get('search_id')

    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM replies WHERE message_id = ?', (search_id,))
        reply = c.fetchone()

    if reply:
        flash(f"Reply: {reply[2]}", 'success')
    else:
        flash("No reply found for the given ID.", 'danger')
    
    return redirect(url_for('index'))

@app.route('/agentlogin', methods=['GET', 'POST'])
def agentlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password').encode('utf-8')

        # Validate with the database and start the session
        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            c.execute('SELECT id, password FROM agents WHERE username = ?', (username,))
            agent = c.fetchone()

            if agent and bcrypt.checkpw(password, agent[1]):
                session['logged_in'] = True
                session['user_id'] = agent[0]  # Storing agent ID in the session
                return redirect(url_for('agent_portal'))

        flash('Invalid username or password!')

    return render_template('agentlogin.html')

@app.route('/agentregister', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password').encode('utf-8')
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO agents (username, password) VALUES (?, ?)', (username, hashed_pw))
                conn.commit()
                flash('Registration successful! Please log in.')
                return redirect(url_for('agentlogin'))
            except sqlite3.IntegrityError:
                flash('Username already exists! Choose another one.')

    return render_template('agentregister.html')

@app.route('/agent_portal')
def agent_portal():
    # Check if the agent is logged in
    if not session.get('logged_in'):
        flash('Please login first!')
        return redirect(url_for('agentlogin'))

    agent_id = session['user_id']

    print("Agent ID: ", agent_id) # For debugging purposes

    # Assign unassigned messages to this agent
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        
        # Fetch an unassigned message
        c.execute('SELECT id FROM customer_messages WHERE id NOT IN (SELECT message_id FROM message_assignments) LIMIT 1')
        message = c.fetchone()

        # If an unassigned message exists, assign it to this agent
        if message:
            message_id = message[0]
            c.execute('INSERT INTO message_assignments (message_id, agent_id, timestamp) VALUES (?, ?, datetime("now"))', (message_id, agent_id))
            conn.commit()

    # Fetch all messages assigned to this agent
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT c.id, c.message, c.timestamp ,c.replied
            FROM customer_messages c 
            INNER JOIN message_assignments a ON c.id = a.message_id 
            WHERE a.agent_id = ? 
            ORDER BY c.timestamp DESC''', (agent_id,))
        messages = c.fetchall()
        
    print("Fetched Messages: ", messages) # For debugging purposes

    return render_template('agents_portal.html', messages=messages)

@app.route('/reply', methods=['POST'])
def reply():
    if 'user_id' not in session:
        return redirect(url_for('agentlogin'))

    if request.method == 'POST':
        message_id = request.form['message_id']
        reply_text = request.form['reply']

        # Check if the message is assigned to the logged-in agent
        agent_id = session['user_id']
        with sqlite3.connect('messages.db') as conn:
            c = conn.cursor()
            c.execute('SELECT agent_id FROM message_assignments WHERE message_id = ?', (message_id,))
            assigned_agent = c.fetchone()

            if assigned_agent and assigned_agent[0] == agent_id:
                # Update the status of the message to 'replied'
                c.execute('INSERT INTO replies (message_id, reply) VALUES (?, ?)', (message_id, reply_text))
                c.execute('UPDATE customer_messages SET replied = TRUE WHERE id = ?', (message_id,))

                # Remove the assignment
                c.execute('DELETE FROM message_assignments WHERE message_id = ?', (message_id,))
                conn.commit()
                flash('Reply sent successfully!', 'success')
            else:
                flash('You are not assigned to this message!', 'danger')

        return redirect(url_for('agent_portal'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You were logged out', 'info')
    return redirect(url_for('agentlogin'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
