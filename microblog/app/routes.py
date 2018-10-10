from flask import render_template
from app import app
@app.route('/')#like springboot 内 的XXXMapping

@app.route('/index')
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
    return render_template('index.html',title='sddd',user=user,posts=posts)
