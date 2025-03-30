from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        amount REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    name = request.form['name']
    amount = request.form['amount']
    if name and amount:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (name, amount) VALUES (?, ?)", (name, amount))
        conn.commit()
        conn.close()
    return home()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
