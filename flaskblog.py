# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 07:34:18 2019

@author: Dilip.Chalamalasetty
"""

from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm,LoginForm

app=Flask(__name__)
app.config['SECRET_KEY']='24fbcde8e1de3d3404d190895b9b4093'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)   #it is not the column it is just the background query

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


posts=[
    {
        'author':'Dilip',
        'title':'Blog post one',
        'content':'First blog   post',
        'date_posted':'April 20, 2018'
    },
    {
        'author':'Durga',
        'title':'Blog post two',
        'content':'second blog   post',
        'date_posted':'April 30, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts,title='Home')

@app.route("/about")
def about():
    return render_template('about.html',title='About')


@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')  #flash is used to display one time required message.
        return redirect(url_for('home'))
    return render_template('register.html',title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if (form.email.data == 'admin@blog.com' and form.password.data == '1234'):
            flash(f'Logged in as admin','success')
            return redirect(url_for('home'))
        else:
            flash(f'username and password is wrong','danger')
    return render_template('login.html',title="Login",form=form)

@app.route("/<user>",methods=['GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if (form.email.data == 'admin@blog.com' and form.password.data == '1234'):
            flash(f'Logged in as admin','success')
            return redirect(url_for('home'))
        else:
            flash(f'username and password is wrong','danger')
    return render_template('login.html',title="Login",form=form)

if __name__=='__main__':
    app.run(debug=True)
    