 cbvfrom flask import Flask, render_template
from flask import session,redirect,url_for#4_5
from flask import flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#SQL
import os
from flask_sqlalchemy import SQLAlchemy

#database backup
from flask_migrate import Migrate

#form
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

#mail
from flask_mail import Mail

basedir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#mail
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')


db=SQLAlchemy(app)
migrate = Migrate(app,db)
mail=Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)




#model
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)
#form
class NameForm(FlaskForm):
    name=StringField('what is your name',validators=[DataRequired()])
    submit=SubmitField('submit')

#set shell
@app.shell_context_processor
def  make_shell_context():
    return dict(db=db,User=User,Role=Role)


#customized error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


#form
@app.route('/',methods=['Get','Post'])
def index():

    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:#is null create
            user=User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known']=False
        else:
            session['known']=True

        session['name']=form.name.data
        form.name.data=''
        # name=form.name.data
        return redirect(url_for('index'))#get

    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))
