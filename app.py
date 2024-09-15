from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla de eventos si no existe
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']
    conn = get_db_connection()
    conn.execute('INSERT INTO events (title, date) VALUES (?, ?)', (title, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:event_id>', methods=['POST'])
def edit_event(event_id):
    title = request.form['title']
    date = request.form['date']
    conn = get_db_connection()
    conn.execute('UPDATE events SET title = ?, date = ? WHERE id = ?', (title, date, event_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
