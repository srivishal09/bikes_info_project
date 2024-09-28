from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('vehicles.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the vehicles table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            fuel_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def main_page():
    return render_template('mainpage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'sri' and password == '12345':
        return redirect(url_for('index'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    id = request.form['id']
    name = request.form['name']
    brand = request.form['brand']
    fuel_type = request.form['fuel-type']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO vehicles (id, name, brand, fuel_type) VALUES (?, ?, ?, ?)', 
                 (id, name, brand, fuel_type))
    conn.commit()
    conn.close()
    
    flash('Vehicle information submitted successfully!')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    search_query = request.args.get('search', '')
    conn = get_db_connection()
    
    if search_query:
        vehicles = conn.execute('SELECT * FROM vehicles WHERE name LIKE ? OR brand LIKE ?', 
                                 ('%' + search_query + '%', '%' + search_query + '%')).fetchall()
    else:
        vehicles = conn.execute('SELECT * FROM vehicles').fetchall()
    
    conn.close()
    return render_template('admin.html', vehicles=vehicles, search_query=search_query)

@app.route('/adminlogin')
def admin_login():
    return render_template('adminlogin.html')

@app.route('/do_admin_login', methods=['POST'])
def do_admin_login():
    admin_username = request.form['adminUsername']
    admin_password = request.form['adminPassword']
    
    if admin_username == 'vishal' and admin_password == '54321':
        return redirect(url_for('admin'))
    else:
        flash('Invalid admin credentials', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM vehicles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Vehicle deleted successfully!')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    init_db()  # Create the database and table if it doesn't exist
    app.run(debug=True)
