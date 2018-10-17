from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm ,RegistrationForm
from flask_login import current_user,login_user
from app.models import User
from flask_login import login_required
#logout
from flask_login import logout_user
#next
from flask import request
from  werkzeug.urls import  url_parse
#for last_seen
from datetime import  datetime
#导入个人信息编辑  10/17
from app.forms import EditProfileForm

@app.route('/')#like springboot 内 的XXXMapping

@app.route('/index')
@login_required#拦截 没登录不能进去
def index():
    user={'username':'Lee'}
    posts=[
    {
     'author':{'username':'jaja'},
     'body':'mew mew!'
    },{
     'author':{'username':'Susan'},
     'body':'exhausted'
    }
    ]
    return render_template('index.html',title='Home Page',posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:#授权跳转到index
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invaild username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        #next
        next_page=request.args.get('next')#！！
        if  not next_page or url_parse(next_page).netloc != '':#不含next/绝对路径
             next_page =url_for('index')
        return redirect(next_page)

    return render_template('login.html',title='Sign In',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return  redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts=[
    {'author':user,'body':'Test post #1'},
    {'author':user,'body':'Test post #2'}
    ]
    return  render_template('user.html',user=user,posts=posts)

#last seen
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.utcnow()#utc 标准时区时间
        #为什么没有用add()  因为引用了current_user
        ''' Flask-Login will invoke the user loader callback function, which will run a database query
        that will put the target user in the database session'''
        #可以写add  但是没必要
        db.session.commit()#提交到数据库

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form =EditProfileForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method=='GET':
        form.username.data =current_user.username
        form.about_me.data=current_user.about_me
    return  render_template('edit_profile.html', title='Edit Profile',form=form)    
