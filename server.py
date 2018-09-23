from flask import Flask
from flask import render_template, request, redirect
from flask_security import Security, logout_user, login_required
from flask_mail import Mail
from flask_security.utils import encrypt_password, verify_password
from flask_restless import APIManager
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore


#database import
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy import or_

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19071999@localhost/women'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'subhailams@gmail.com',
    MAIL_PASSWORD = 'Subha@1999',
)


mail = Mail()
mail.init_app(app)
db = SQLAlchemy(app)

5
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

class Empscheme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    schname = db.Column(db.String(255), unique=True)
    schdescrip =  db.Column(db.String(255), unique=True)
    site = db.Column(db.String(255))

    def __repr__(self):
        return '<Empscheme %r>' % self.schname

class Healthscheme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    schname = db.Column(db.String(255), unique=True)
    schdescrip =  db.Column(db.String(255), unique=True)
    site = db.Column(db.String(255))

    def __repr__(self):
        return '<Empscheme %r>' % self.schname

class Educationscheme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    schname = db.Column(db.String(255), unique=True)
    schdescrip =  db.Column(db.String(255), unique=True)
    site = db.Column(db.String(255))

    def __repr__(self):
        return '<Empscheme %r>' % self.schname

class Bankingscheme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    schname = db.Column(db.String(255), unique=True)
    schdescrip =  db.Column(db.String(255), unique=True)
    site = db.Column(db.String(255))

    def __repr__(self):
        return '<Empscheme %r>' % self.schname

class Socialsecurityscheme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    schname = db.Column(db.String(255), unique=True)
    schdescrip =  db.Column(db.String(255), unique=True)
    site = db.Column(db.String(255))

    def __repr__(self):
        return '<Empscheme %r>' % self.schname

class legalsupportscheme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    schname = db.Column(db.String(255), unique=True)
    schdescrip =  db.Column(db.String(255), unique=True)
    site = db.Column(db.String(255))

    def __repr__(self):
        return '<Empscheme %r>' % self.schname




# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Views 
@app.route('/')
def home():
    user=User.query.all()
    return render_template('index.html',user= user)


@app.route('/employment')
@login_required
def employment():
    res= Empscheme.query.all()
    return render_template('employment.html', res=res)

@app.route('/healthcare')
@login_required
def healthcare():
    res= Healthscheme.query.all()
    return render_template('healthcare.html', res=res)


@app.route('/banking')
@login_required
def banking():
    res= Bankingscheme.query.all()
    return render_template('banking.html', res=res)

@app.route('/socialsecurity')
@login_required
def socialsecurity():
    res= Socialsecurityscheme.query.all()
    return render_template('socialsecurity.html', res=res)


@app.route('/education')
@login_required
def education():
    res= Educationscheme.query.all()
    return render_template('education.html', res=res)


@app.route('/legalsupport')
@login_required
def legalsupport():
    res= legalsupportscheme.query.all()
    return render_template('legalsupport.html', res=res)


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


# Start server 
if __name__ == '__main__':
    app.run()
