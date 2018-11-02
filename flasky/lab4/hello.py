from flask import Flask, render_template
from flask import session,redirect,url_for#4_5
from flask import flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

#form
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

#form
class NameForm(FlaskForm):
    name=StringField('what is your name',validators=[DataRequired()])
    submit=SubmitField('submit')


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
    name=None
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        if old_name is not None and old_name !=form.name.data:
            flash('look like you have changed your name!')
        session['name']=form.name.data
        # name=form.name.data
        return redirect(url_for('index'))#get

    return render_template('index.html',form=form,name=session.get('name'))
