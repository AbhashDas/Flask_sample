from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PHOE@nix11'
app.config['MYSQL_DB'] = 'devops5'

mysql = MySQL(app)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hash the password before storing it in the database
        # You can use libraries like Werkzeug for password hashing
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_list (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_list WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            # User authenticated, redirect to home page or dashboard
            return redirect(url_for('index'))
        else:
            # Invalid credentials, redirect back to login page
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
