from flask import Flask, request, jsonify, render_template, flash, redirect, url_for

import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS customer_messages
                     (id INTEGER PRIMARY KEY, message TEXT, replied BOOLEAN DEFAULT FALSE,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS replies
                     (id INTEGER PRIMARY KEY, message_id INTEGER, reply TEXT)''')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO customer_messages (message) VALUES (?)', (message,))
        flash('Message sent successfully!')
    return redirect(url_for('index'))
    #return "Message sent!", 200

@app.route('/agent')
def agent_portal():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.row_factory = sqlite3.Row
        messages = c.execute('SELECT * FROM customer_messages ORDER BY timestamp DESC').fetchall()
    return render_template("agent_portal.html", messages=messages)

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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
