from flask import Flask
@app.route('/')

def index():
    user_agent=request.headers.get('User_agent')
    return '<p>Your browers is {}</p>'.format(user_agent)
