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
                     (id INTEGER PRIMARY KEY, message_id INTEGER, reply TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS agents (id INTEGER PRIMARY KEY,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL )''')

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
    #return "Message sent!", 200
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
            c.execute('SELECT password FROM agents WHERE username = ?', (username,))
            hashed_pw = c.fetchone()

            if hashed_pw and bcrypt.checkpw(password, hashed_pw[0]):
                session['logged_in'] = True
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



@app.route('/agent')
def agent_portal():
    if not session.get('logged_in'):
        flash('Please login first!')
        return redirect(url_for('agentlogin'))
    
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        messages = c.execute('SELECT * FROM customer_messages ORDER BY timestamp ASC').fetchall()
    return render_template("agents_portal.html", messages=messages)

@app.route('/reply', methods=['POST'])
def reply():
    message_id = request.form.get('message_id')
    reply_text = request.form.get('reply')
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO replies (message_id, reply) VALUES (?, ?)', (message_id, reply_text))
        c.execute('UPDATE customer_messages SET replied = TRUE WHERE id = ?', (message_id,))
        flash('Reply sent successfully!')
    return redirect(url_for('agent_portal'))
    #return "Reply sent!", 200

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('You were logged out', 'info')
    return redirect(url_for('agentlogin')) # redirect to login page after logging out

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
