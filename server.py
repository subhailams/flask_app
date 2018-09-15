from flask import Flask
from flask import render_template, request, redirect
from flask_security import Security, logout_user, login_required
from flask_security.utils import encrypt_password, verify_password
from flask_restless import APIManager
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

from admin import init_admin

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19071999@localhost/women'
app.config['SECRET_KEY'] = 'super-secret'



db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Views 
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/mypage')
@login_required
def mypage():
    return render_template('mypage.html')


@app.route('/logout')
def log_out():
    logout_user()
    return redirect(request.args.get('next') or '/')

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))
# Start server  ===============================================================
if __name__ == '__main__':
    app.run()
