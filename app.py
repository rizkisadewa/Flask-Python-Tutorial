from flask import Flask, render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from data import Articles #import the data from data.py
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#use the function of Article() so that we can return the value of the data
Articles = Articles()

# Create a route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

# Form Validator for Register
class RegisterFrom(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6, max=50)])
    password = StringField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

#route for register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterFrom(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create a cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s,%s,%s,%s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        username = request.form('username')
        password_candidate = request.form('password')

        # Create cursor
        cur = mysql.connection.cursor()

        #Get user by Username
        result = cur.execute("SELECT FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info("PASSWORD MATCHED")
            else:
                app.logger.info("PASSWORD NOT MATCHED")
        else:
            app.loger.info("NO USER")

    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
