from flask import Flask, render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from data import Articles #import the data from data.py
from flaskext.mysql import MySQL # import from MYSQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
#use the function of Article() so that we can return the value of the data
Articles = Articles()

mysql = MySQL()

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
        return render_template('register.html')
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
