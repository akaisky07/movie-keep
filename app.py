import datetime
import sqlite3
from flask import Flask, render_template, request, g, redirect

app = Flask(__name__)

# Create a function to connect to the database
def connect_db():
    sql = sqlite3.connect('todo.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Create a function to initialize the database
@app.before_first_request
def create_table():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, task TEXT, timestamp DATETIME)')
    db.commit()

@app.route('/')
def index():
    db = get_db()
    todos = db.execute('SELECT * FROM todo ORDER BY timestamp DESC').fetchall()
    return render_template('index.html', todos=todos, datetime=datetime)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    timestamp = datetime.datetime.now()
    db = get_db()
    db.execute('INSERT INTO todo (task, timestamp) VALUES (?, ?)', [task, timestamp])
    db.commit()
    return redirect('/')
    
@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', [id])
    db.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)

